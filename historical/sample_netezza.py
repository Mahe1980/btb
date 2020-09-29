from src.core.connectors.connectors import get_nz_conn
import pandas as pd
import argparse
import json
import re
import os


NZ_TO_DATASET_DTYPE_MAPPING = {
    'bigint': 'int64',
    'integer': 'int64',
    'byteint': 'int64',
    'smallint': 'int64',
    'double precision': 'float64',
    'numeric': 'float64',
    'timestamp': 'datetime64',
    'string': 'str'
}
CHUNKSIZE = 1000000


def convert_dtype(df, table):
    with open('./manifest/{}.json'.format(table)) as f:
        d = json.load(f)['fields']
        for data in d:
            col = data['name']
            dw_dtype = data['dtype']
            df_dtpye = df[col].dtype.name
            if df_dtpye != 'object' and not re.search(df_dtpye[:10], NZ_TO_DATASET_DTYPE_MAPPING[dw_dtype]):
                if df_dtpye == 'float64' and NZ_TO_DATASET_DTYPE_MAPPING[dw_dtype] == 'int64':
                    print('casting from {} to Int64 for {}'.format(df_dtpye, col))
                    df[col] = df[col].astype('Int64')
    return df


def extract(table, from_ts, to_ts, chunksize, output_dir):
    conn = get_nz_conn()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if os.path.isfile('{}/{}.json'.format(output_dir, table)):
        os.remove('{}/{}.json'.format(output_dir, table))

    with open('./sql/{}.sql'.format(table)) as f, open('{}/{}.json'.format(output_dir, table), mode='a') as fw:
        sql = f.read().format(from_ts=from_ts, to_ts=to_ts)
        ichunks = pd.read_sql_query(sql, conn, chunksize=chunksize)
        for df in ichunks:
            df_p = convert_dtype(df, table)
            df_p.to_json(fw, orient="records", date_format='iso', date_unit='s', lines=True)
            fw.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('table', help='Table Name to extract')
    parser.add_argument('--from_ts', default='1900-01-01 00:00:00', help='From Timestamp')
    parser.add_argument('to_ts', help='To Timestamp')
    parser.add_argument('--chunksize', default=CHUNKSIZE, help='pandas chunk size')
    parser.add_argument('--output_dir', default="./output/", help='output directory')
    args = parser.parse_args()
    extract(**vars(args))
