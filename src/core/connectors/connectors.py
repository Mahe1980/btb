from src.core.connectors.nz import NZConnector
from src.core.connectors.oracle import OracleConnector
from src.core.connectors.encryptor import aes_encrypt_pass
from src.settings import envs

import cx_Oracle
from collections import namedtuple
import logging
from src.settings import log_config
logger = logging.getLogger(__name__)


def get_connector():
    """
    Gets connection for CTL DB
    :return: conn object
    """
    hostname = envs.HOSTNAME
    sid = envs.SID
    port = envs.PORT
    user = envs.USER
    password = envs.PASSWORD
    password = aes_encrypt_pass(password)

    db_uri = '{user}/{password}@{hostname}:{port}/{sid}'

    db_uri = db_uri.format(user=user,
                           password=password,
                           hostname=hostname,
                           port=port,
                           sid=sid)

    conn = cx_Oracle.connect(db_uri)

    return conn


def get_conn_details(c_name):
    """
    Connect to a sql type DB. Must supply name of connection from CTL_CONNET table
    :return: results (named tuples)
    """

    sql = """select NAME, TYPE, AUTH_TYPE, HOSTNAME, SID_DB, PORT_NUMBER, USERNAME, PASSWORD from ctl_connect where name 
    = :c_name"""

    conn = get_connector()
    cursor = conn.cursor()

    cursor.execute(sql, c_name=c_name)

    conn_details = namedtuple('conn_details', 'name, conn_type, auth_type, hostname, sid_db, port, user, password')
    rows = list(cursor.fetchall()[0])
    rows[-1] = aes_encrypt_pass(rows[-1])  # decrypt the password
    conn_details = conn_details(*rows)

    logger.debug("Collected connection details successfully")

    conn.close()

    return conn_details


def get_nz_conn():
    """
    Connector for Netezza
    :return: conn object
    """
    conn_name = envs.NZ_CTL_CONN_NAME
    conn_details = get_conn_details(conn_name)

    conn = NZConnector(user=conn_details.user,
                       password=conn_details.password,
                       hostname=conn_details.hostname,
                       db=conn_details.sid_db,
                       port=conn_details.port).get_engine()

    logger.info("Connection to NZ created successfully")

    return conn


def get_oracle_conn():
    """
    Connector for Oracle
    :return: conn object
    """
    conn_name = envs.ORACLE_CTL_CONN_NAME
    conn_details = get_conn_details(conn_name)

    conn = OracleConnector(user=conn_details.user,
                           password=conn_details.password,
                           hostname=conn_details.hostname,
                           sid=conn_details.sid_db,
                           port=conn_details.port).get_engine()

    logger.info("Connection to Oracle created successfully")

    return conn
