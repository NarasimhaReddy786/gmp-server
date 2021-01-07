from flask_restful import Resource
from config import db_connector
import base64
from flask import Flask, jsonify, request

class StoreLocation(Resource):
    def __init__(self):
        print("Inside StoreLocation")


    def post(self):
        json_data = request.get_json(force=True)

        database_name = "gmp_db"
        collection_gmp = "gmp_locations"

        conn = db_connector.Connection()
        client = conn.getConnection()
        db = client[database_name]
        collection_maps = db[collection_gmp]

        cursor = collection_maps.insert({"location":json_data})

        return 'Success'