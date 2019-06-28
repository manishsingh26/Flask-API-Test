
import re
import os
from flask import Flask
from flask_restful import Api
from flask_restful import Resource
from flask_restful import reqparse
from werkzeug.datastructures import FileStorage

from Alice.ml_operation.ml_main import TriggerOperation

app = Flask(__name__)
api = Api(app)


class StatusCheck(Resource):
    def get(self):
        return {"message": "PCAP Operation", "status": "success"}


upload_folder = r"C:\Users\m4singh\Documents\Logs\PycharmProjects\API-PCAP\Alice\input"
parser = reqparse.RequestParser()
parser.add_argument("file", type=FileStorage, location="files")


class ZipUpload(Resource):
    def post(self):
        data = parser.parse_args()

        if data["file"] == "":
            return {"message": "No file found", "status": "error"}

        zip_data = data['file']
        if zip_data:
            split_first = str(data).split(".")[0]
            file_name = re.split("FileStorage:", split_first)[-1].strip().replace("'", "") + ".zip"
            zip_complete_path = os.path.join(upload_folder, file_name)
            zip_data.save(zip_complete_path)
            return {"message": "photo uploaded", "status": "success", "path": zip_complete_path}
        return {"message": "Something when wrong", "status": "error"}


api.add_resource(StatusCheck, "/")
api.add_resource(ZipUpload, "/upload")
api.add_resource(TriggerOperation, "/trigger/<string:file_name>")


if __name__ == "__main__":
    app.run()
