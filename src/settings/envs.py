import os
import json


env = os.environ.get('ENV')

NZ_TO_DATASET_DTYPE_MAPPING = {
    'bigint': 'int64',
    'integer': 'int64',
    'byteint': 'int64',
    'smallint': 'int64',
    'double precision': 'float64',
    'numeric': 'float64',
    'numeric(15,2)': 'float64',
    'timestamp': 'datetime64',
    'string': 'str'
}

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CURRENT_DIR = os.path.dirname(__file__)


with open('{}/envs.json'.format(CURRENT_DIR)) as f:
    d = json.load(f)
    HOSTNAME = d[env]["hostname"]
    SID = d[env]["sid"]
    USER = d[env]["user"]
    OWBER = d[env]["owner"]
    PASSWORD = d[env]["password"]

    # Connection Name
    NZ_CTL_CONN_NAME = d[env]["nz_ctl_conn_name"]
    ORACLE_CTL_CONN_NAME = d[env]["oracle_ctl_conn_name"]

    # Common
    PORT = d["common"]["port"]
    DEFAULT_CHUNK = d["common"]["default_chunk"]
