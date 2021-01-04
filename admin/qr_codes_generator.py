import logging
from flask_restful import Resource
from config import db_connector
import qrcode
import zipfile
import os
from flask import send_file

logger = logging.getLogger('shortest_path')

class Generate_qr_codes(Resource):

    def __init__(self):
        logger.debug("Inside Generating QR codes init")

    def get(self, loc_id):
        database_name = "gmp_db"
        collection_gmp = "gmp_locations"
        try:
            conn = db_connector.Connection()
            client = conn.getConnection()
            db = client[database_name]
            collection_locations = db[collection_gmp]
            cursor = collection_locations.find_one({"_id": int(loc_id)})

            os.mkdir('temp')
            for document in cursor["positions"]:
                if "Y" == document["destination"]:
                    position_name = document["position_name"]
                    position_id = document["position_id"]
                    img = qrcode.make(str(loc_id)+'/'+str(position_id))
                    print(img)
                    img.save('temp/'+str(position_name)+'.png')

            # removes old zip file
            os.remove("qr_codes.zip")
            # Zip file Initialization
            zip_folder = zipfile.ZipFile('qr_codes.zip', 'w', compression=zipfile.ZIP_STORED)  # Compression type

            # zip all the files which are inside in the folder
            for root, dirs, files in os.walk('temp/'):
                for file in files:
                    zip_folder.write('temp/'+file)
            zip_folder.close()

            return send_file('qr_codes.zip',
                             mimetype='zip',
                             attachment_filename='qr_codes.zip',
                             as_attachment=True)
            logger.debug("sent zip file successfully")
        except Exception as e:
            logger.error("Error while generating QR codes with trace back :%s", e)
        finally:
            conn.closeConnection()
            os.rmdir('temp')
