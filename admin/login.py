import logging
from flask_restful import Resource
from config import db_connector

logger = logging.getLogger('shortest_path')


class Login(Resource):

    def __init__(self):
        logger.debug("Inside Shortest_Path")

    def get(self, username, password):
        logger.debug("login validation with username: %s, and password: %s", username, password)
        database_name = "gmp_db"
        collection_gmp = "gmp_admin_cred"

        conn = db_connector.Connection()
        client = conn.getConnection()
        db = client[database_name]
        admin_cred_collection = db[collection_gmp]
        cursor = admin_cred_collection.find_one({"username": username, "password": password})

        if cursor== None:
            logger.debug("Invalid admin cred")
            return False
        else:
            logger.debug("valid admin cred")
            return True
