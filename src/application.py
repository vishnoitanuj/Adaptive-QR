import os
from flask import Flask, request, url_for
from flask_cors import CORS
from flask_restx import Resource, Api, reqparse
from qrGenerator import QRGenerator


class SecureApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'http' if '8080' in self.base_url else 'https'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)

app = Flask(__name__)
api = SecureApi(app)
CORS(app, support_credentials=True)
PORT = int(os.getenv('PORT', 8080))

parser = reqparse.RequestParser()
parser.add_argument('data', type=dict)
parser.add_argument('index', type=str)

@api.route('/makeQr', endpoint='with-parser')
class QRMaker(Resource):
    def post(self):
        req_body = request.get_json(force=True)
        qr_data = req_body['qr_data']
        index = req_body['index']
        # try:
        qrGenerator = QRGenerator(qr_data, index)
        return {'image': str(qrGenerator.make_qr())}
        # except Exception as e:
        #     print("Error = ", str(e))
        #     return "Error Occured" 

api.add_resource(QRMaker, '/makeQr')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, threaded=True)
