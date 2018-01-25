# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import main
import os

# flaskの設定
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/api", methods=['GET'])
def index():
    response = ""
    url = request.args.get("url")
    if not (url is None):
        main.start(url)
        response = jsonify({'message': "File is uploaded GoogleDrive"})
        response.status_code = 200

    else:
        response = jsonify({'message': "You must append '/api?url=Youtube_URL'"})
        response.status_code = 404

    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
