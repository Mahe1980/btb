import cx_Oracle
import logging


logger = logging.getLogger(__name__)


class OracleConnector(object):

    """
    A cx_Oracle powered DB-API connector to read and write data.
    """

    def __init__(self,
                 user,
                 password,
                 hostname,
                 sid,
                 port):

        self.user = user
        self.password = password
        self.hostname = hostname
        self.port = port
        self.sid = sid

    @property
    def db_uri(self):
        """
        Forms DB uri
        :return: db_uri:str
        """

        db_uri = '{user}/{password}@{hostname}:{port}/{sid}'

        db_uri = db_uri.format(user=self.user,
                               password=self.password,
                               hostname=self.hostname,
                               port=self.port,
                               sid=self.sid)

        return db_uri

    def get_engine(self):
        """
        Gets engine for Oracle
        :return: engine
        """

        logger.debug("db_uri: {}".format(self.db_uri))

        engine = cx_Oracle.connect(self.db_uri)

        logger.debug("get_engine: {}".format(engine))

        return engine
