import pyodbc
import logging


logger = logging.getLogger(__name__)


class NZConnector(object):

    """
    A pyodbc powered DB-API connector to read and write data.
    """

    def __init__(self,
                 user,
                 password,
                 hostname,
                 db,
                 port,
                 driver='NetezzaSQL'):

        self.user = user
        self.password = password
        self.hostname = hostname
        self.port = port
        self.db = db
        self.driver = driver

    @property
    def db_uri(self):
        """
        Forms db uri
        :return: db_uri:str
        """

        db_uri = "DRIVER={driver};"

        db_uri += 'SERVERNAME={hostname};PORT={port};DATABASE={db};USERNAME={user};PASSWORD={password}'

        db_uri = db_uri.format(hostname=self.hostname,
                               port=self.port,
                               db=self.db,
                               user=self.user,
                               password=self.password,
                               driver=self.driver)

        return db_uri

    def get_engine(self):
        """
        Gets engine for NZ
        :return: engine
        """

        logger.debug("db_uri: {}".format(self.db_uri))

        engine = pyodbc.connect(self.db_uri)

        logger.debug("get_engine: {}".format(engine))

        return engine
