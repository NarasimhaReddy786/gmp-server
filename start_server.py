from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from user import get_shortest_path, all_locations, get_paths
from admin import store_location
from admin import qr_codes_generator

import logging.handlers

app = Flask("GMP Server")
api = Api(app)
CORS(app)

file_name = "shortest_path.log"
logger = logging.getLogger('shortest_path')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.handlers.TimedRotatingFileHandler(filename=file_name, utc=False, when='midnight', interval=1, backupCount=0)
fh.suffix = "%Y-%m-%d"
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
formatter = logging.Formatter('%(asctime)-s %(message)s')
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(fh)


# to get all locations in company/hospital/building takes Id
api.add_resource(all_locations.AllLocations, '/destination_list/<loc_id>/<pos_id>')

api.add_resource(get_paths.GetPaths, '/shortest_path/<loc_id>/<source>/<destination>/<path_type>/<random_number>')

api.add_resource(store_location.StoreLocation, '/store_location')

api.add_resource(qr_codes_generator.Generate_qr_codes, '/get_qr_codes/<loc_id>')


if __name__ == '__main__':
  logger.info("starting server")
  app.run(debug=True)