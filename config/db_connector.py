import _thread
import logging
from pymongo import MongoClient
from config import read_properties

logger = logging.getLogger('shortest_path')

class Connection:

    def __init__(self):
       pass

    client = None
    # read the db connection ip and port details
    @staticmethod
    def readUrl(self):
        return read_properties.read("config\dbconfig.properties")

    # read the admin user password to authenticate
    @staticmethod
    def readAdminPassword(self):
            return read_properties.read("config\dbadmin.properties")

    # connect to mongo db
    def connect_db(self):
        try:
            #url = self.readUrl(self)
            #host_from_props = url['mongodburlIP'][0]
            #port_from_props = url['mongodburlPORT'][0]
            logger.info("Thread Id " + str(_thread.get_ident()) + " Initiating DB connection")
            client = MongoClient("mongodb+srv://admin:admin@cluster0.4tlbt.mongodb.net/gmp_db?retryWrites=true&w=majority")
            # db = client["admin"]
            #admin_password = self.readAdminPassword(self)['password'][0]
            # db.authenticate("admin", admin_password);
            logger.info(client.server_info())
            logger.info("Thread Id " + str(_thread.get_ident()) + " DB connection Established")
            return client
        except BaseException as e:
            logger.error("Thread Id " + str(_thread.get_ident()) + " Error when connection to DataBase :" + str(e),
                         exc_info=True)
            raise

    def closeConnection(self):
            self.client.close()
            self.client = None
            logger.info("Thread Id " + str(_thread.get_ident()) + " DB connection Closed")

    def getConnection(self):
        if self.client == None:
            logger.info("self.client is None")
            self.client = self.connect_db()
            return self.client
        else:
            return self.client
