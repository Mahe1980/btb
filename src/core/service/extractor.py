import json
import pandas as pd
import re
from pathlib import Path
from src.core.connectors.connectors import get_nz_conn
from src.settings.envs import NZ_TO_DATASET_DTYPE_MAPPING
from src.settings import envs
from src.settings import log_config
import logging

logger = logging.getLogger(__name__)


class Extractor(object):

    def __init__(self, source, cutoff_ts):
        self.source = source
        self.cutoff_ts = cutoff_ts
        self.conn = get_nz_conn()

    def run(self, output_path):
        """
        This extracts data from NZ and generates json output
        :param output_path:
        """
        sql = self.prepare_extract_query()
        logger.info("sql query to extract data from NZ '{}'".format(sql))
        chunk_size = envs.DEFAULT_CHUNK if self.source.chunk_size is None else self.source.chunk_size
        with open(output_path, mode="a") as fw:
            df_chunks = pd.read_sql_query(sql=sql, con=self.conn, chunksize=chunk_size)
            for df in df_chunks:
                df_c = self.convert_types(df)
                df_c.to_json(fw, orient="records", date_format='iso', date_unit='s', lines=True)
                fw.write('\n')
        logger.info("Extracted json output file '{}'".format(Path(output_path).name))

    def convert_types(self, df):
        """
        Converts Float64 to Int64 if the actual dtype is Int64 and there are NaN (pandas bug)
        :param df:
        :return: df
        """
        manifest_file = "{}/{}/{}.json".format(envs.PROJECT_ROOT, "src/core/manifest", self.source.source_name)
        with open(manifest_file) as f:
            man_fields = json.load(f)["fields"]
            for man_field in man_fields:
                man_field_name, man_field_type = man_field["name"], man_field["dtype"]
                df_dtpye = df[man_field_name].dtype.name
                man_dtype = NZ_TO_DATASET_DTYPE_MAPPING.get(man_field_type)
                if df_dtpye != "object" and not re.search(df_dtpye[:10], man_dtype):
                    if df_dtpye == "float64" and man_dtype == "int64":
                        logger.info(("Casting {} to Int64 for {}".format(df_dtpye, man_field_type)))
                        df[man_field_name] = df[man_field_name].astype("Int64")
        return df

    def prepare_extract_query(self):
        """
        Prepares extract sql query for extraction
        :return: sql (string)
        """
        table = self.source.source_name
        wm_columns = self.source.watermark_columns
        wm_value = self.source.value
        fields = self.source.select_fields
        where_filter = "" if self.source.where_filter is None else " AND " + self.source.where_filter

        sql = "SELECT {fields} FROM {table} WHERE ".format(fields=fields, table=table)
        watermark = self.prepare_watermark(wm_columns, wm_value)

        sql += "{wm}{wf}".format(wm=watermark, wf=where_filter)
        return sql

    def prepare_watermark(self, hwm_columns, hwm_value):
        """
        Prepares WM part for the sql query
        :param hwm_columns:
        :param hwm_value:
        :return: hwm_clause (string)
        """
        cols = json.loads(hwm_columns)["cols"]
        from_ts = json.loads(hwm_value)["HWM1"]

        hwm_clause = ''
        for col in cols:
            hwm_clause += "({col} >= '{from_ts}' AND {col} < '{to_ts}') OR ".format(col=col, from_ts=from_ts,
                                                                                    to_ts=self.cutoff_ts)

        hwm_clause = hwm_clause[:-4]

        return hwm_clause
