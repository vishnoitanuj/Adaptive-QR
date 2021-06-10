import os
from flask import Flask, request, url_for
# from flask_cors import CORS
from flask_restx import Api
from src.qrGenerator import QRGenerator


class SecureApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'http' if '8080' in self.base_url else 'https'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)

app = Flask(__name__)
# CORS(app, support_credentials=True)

@app.route('/makeQr', methods = ['GET', 'POST'])
def qrMaker():
    if request.method == 'POST':
        req_body = request.json
        qr_data = req_body['qr_data']
        index = req_body['index']
        try:
            qrGenerator = QRGenerator(qr_data, index)
            return {'image': str(qrGenerator.make_qr())}
        except Exception as e:
            print("Error = ", str(e))
            return "Error Occured" 

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
