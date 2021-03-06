from flask_restful import Resource
from config import db_connector
from bson.objectid import ObjectId


class AllLocations(Resource):
    def __init__(self):
        print("Inside All_Locations")

    def get(self, loc_id, pos_id):
        database_name = "gmp_db"
        collection_gmp = "gmp_locations"

        conn = db_connector.Connection()
        client = conn.getConnection()
        db = client[database_name]
        collection_locations = db[collection_gmp]
        cursor = collection_locations.find_one({"_id": ObjectId(loc_id)})

        locationObj = cursor["location"]

        json_response = {}
        location = {}
        location["locationId"] = str(cursor["_id"])
        location["locationName"] = locationObj["location_name"]
        json_response["location"] = location
        
        destinations = []
        for document in locationObj["positions"]:
            position_name = document["position_name"]
            position_id = document["position_id"]
            is_destination = document["destination"]
            if position_id != int(pos_id) and "N" != is_destination:
                destination = {}
                destination["positionId"] = position_id
                destination["positionName"] = position_name
                destinations.append(destination)
            elif position_id == int(pos_id) and "N" != is_destination:
                source = {}
                source["positionId"] = position_id
                source["positionName"] = position_name
                json_response["source"] = source

        try:
            amenitiesFromDb = locationObj["amenities"]
            amenities = []
            for document in amenitiesFromDb:
                amenity = {}
                amenity["positionId"] = document["position_id"]
                amenity["positionName"] = document["position_name"]
                amenities.append(amenity)
            json_response["amenities"] = amenities
        except KeyError:
            pass


        json_response["detinations"] = destinations
        
        return json_response
