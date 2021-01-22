from flask_restful import Resource
from admin import generate_all_possible_paths
import logging
from PIL import Image, ImageDraw
from flask import send_file, make_response
import io
from config import db_connector
from bson.objectid import ObjectId
import base64
from io import BytesIO
from base64 import b64decode

logger = logging.getLogger('shortest_path')


class GetPaths(Resource):

    def __init__(self):
        print("Inside GetPaths")

    def get(self, loc_id, source, destination, path_type, random_number):
        logger.info(" Request for paths came with location id: %s ,source id:%s and desination id :%s ", str(loc_id), source, destination)

        if path_type == 'A' or path_type == 'S':
            shortest_path_with_coordinates = generate_all_possible_paths.get_preferred_path(loc_id, int(source), int(destination), 'S')

        if path_type == 'A' or path_type == 'L':
            longest_path_with_coordinates = generate_all_possible_paths.get_preferred_path(loc_id, int(source), int(destination), 'L')

        database_name = "gmp_db"
        collection_gmp = "gmp_locations"

        conn = db_connector.Connection()
        client = conn.getConnection()
        db = client[database_name]
        collection_locations = db[collection_gmp]
        cursor = collection_locations.find_one({"_id": ObjectId(loc_id)})

        locationObj = cursor["location"]

        imageString = locationObj["map"]

        im = Image.open(BytesIO(b64decode(imageString.split(',')[1])))
        draw = ImageDraw.Draw(im)

        if path_type == 'A' or path_type == 'L':
            lengthOfCoordinatesArray = len(longest_path_with_coordinates)
            for arrayIndex in range(lengthOfCoordinatesArray):
                if arrayIndex == 0:
                    pass
                else:
                    draw.line(((longest_path_with_coordinates[arrayIndex-1]['x'], longest_path_with_coordinates[arrayIndex-1]['y']), 
                        (longest_path_with_coordinates[arrayIndex]['x'], longest_path_with_coordinates[arrayIndex]['y'])), 
                        fill=(204, 170, 0), width=8)
                    if arrayIndex == lengthOfCoordinatesArray-1:
                        pinImage = Image.open('destinationPin.png')
                        im.paste(pinImage, (longest_path_with_coordinates[arrayIndex]['x'], longest_path_with_coordinates[arrayIndex]['y']))

        if path_type == 'A' or path_type == 'S':
            lengthOfCoordinatesArray = len(shortest_path_with_coordinates)
            for arrayIndex in range(lengthOfCoordinatesArray):
                if arrayIndex == 0:
                    pass
                else:
                    draw.line(((shortest_path_with_coordinates[arrayIndex-1]['x'], shortest_path_with_coordinates[arrayIndex-1]['y']), 
                        (shortest_path_with_coordinates[arrayIndex]['x'], shortest_path_with_coordinates[arrayIndex]['y'])), 
                        fill=(7, 149, 25), width=8)
                    if arrayIndex == lengthOfCoordinatesArray-1:
                        pinImage = Image.open('destinationPin.png')
                        im.paste(pinImage, (shortest_path_with_coordinates[arrayIndex]['x'], shortest_path_with_coordinates[arrayIndex]['y']))

        im.save("MapWithRoute.png")
        return send_file("MapWithRoute.png", mimetype='image/jpg', attachment_filename='python.jpg')
