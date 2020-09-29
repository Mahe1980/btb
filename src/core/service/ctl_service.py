import pandas as pd
from src.core.service.source import Source
from src.core.connectors.connectors import get_oracle_conn
from src.settings import log_config
import logging
logger = logging.getLogger(__name__)


class CTLService(object):

    def __init__(self, scope, frequency, source_name=None):
        self.scope = scope
        self.frequency = frequency
        self.source_name = source_name
        self.conn = get_oracle_conn()

    def get_sources(self):
        sql = self.prepare_query()
        logger.info("sql query to get sources '{}'".format(sql))
        rows = pd.read_sql_query(sql, self.conn)
        sources = [
            Source(row.SCOPE,
                   row.SOURCE_NAME,
                   row.SOURCE_TYPE,
                   row.DB_TYPE,
                   row.LOAD_TYPE,
                   row.FREQUENCY,
                   row.STATE,
                   row.STATUS,
                   row.BATCH_SIZE,
                   row.PARALLELIZE,
                   row.WATERMARK_COLUMNS,
                   row.VALUE,
                   row.SELECT_FIELDS,
                   row.WHERE_FILTER,
                   row.LAST_SUCCESS_TS,
                   row.LAST_RUN_TS
                   )
            for row in rows.itertuples()
        ]

        return sources

    def prepare_query(self):
        sql = """SELECT * FROM CTL_GCP_MIGRATION WHERE SCOPE='{scope}' and FREQUENCY='{frequency}' and STATUS='on'""".\
            format(scope=self.scope, frequency=self.frequency)
        if self.source_name:
            sql += " and SOURCE_NAME='{source_name}'".format(source_name=self.source_name)
        return sql

    def update_field(self, field, value):
        sql = self.prepare_update_sql(field)
        logger.info("sql query to update '{}' column for '{}'".format(field, sql))
        cursor = self.conn.cursor()
        cursor.execute(sql, {"value": value})
        self.conn.commit()

    def prepare_update_sql(self, field):
        sql = """UPDATE CTL_GCP_MIGRATION SET {field}=(:value) WHERE SOURCE_NAME='{source_name}'""". \
            format(field=field, source_name=self.source_name)
        return sql
