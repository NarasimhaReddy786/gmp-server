from flask_restful import Resource
from config import db_connector
from bson.objectid import ObjectId


class AllLocationNames(Resource):
    def __init__(self):
        print("Inside AllLocationNames")

    def get(self):
        database_name = "gmp_db"
        collection_gmp = "gmp_locations"

        client = db_connector.Connection()
        connection = client.getConnection()
        database = connection[database_name]
        collection = database[collection_gmp]

        cursor = collection.find({})

        response = {}
        locations = []

        for document in cursor:
            location = {}
            db_location = document["location"]
            location["location_id"] = str(document["_id"])
            location["location_name"] = db_location["location_name"]
            locations.append(location)
        
        response["locations"] = locations
        return response