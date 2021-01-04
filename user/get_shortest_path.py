from flask_restful import Resource
from admin import generate_all_possible_paths
import logging
from PIL import Image, ImageDraw
from flask import send_file, make_response

logger = logging.getLogger('shortest_path')


class ShortestPath(Resource):

    def __init__(self):
        logger.debug("Inside Shortest_Path")

    def get(self, loc_id, source, destination, random_number):
        logger.info(" Request for shortest path came with location id: %s ,source id:%s and desination id :%s ",
                    loc_id, source, destination)

        shortest_path_with_coordinates = generate_all_possible_paths.get_path(int(loc_id), int(source), int(destination))
        logger.info("Responded with : %s", shortest_path_with_coordinates)
        im = Image.open("TietoEvryMap.png")
        draw = ImageDraw.Draw(im)

        lengthOfCoordinatesArray = len(shortest_path_with_coordinates)
        for arrayIndex in range(lengthOfCoordinatesArray):
            if arrayIndex == 0:
                pass
            else:
                draw.line(((shortest_path_with_coordinates[arrayIndex-1]['x'], shortest_path_with_coordinates[arrayIndex-1]['y']), (shortest_path_with_coordinates[arrayIndex]['x'], shortest_path_with_coordinates[arrayIndex]['y'])), fill=(0, 192, 192), width=8)

        #draw.line(((181, 117), (181, 177), (949, 177), (949, 288)), fill=(0, 192, 192), width=8)
        im.save("TietoEvryPath.png")
        return send_file("TietoEvryPath.png", mimetype='image/jpg', attachment_filename='python.jpg')
