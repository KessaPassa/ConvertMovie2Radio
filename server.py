 # -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, url_for, abort, Response
import os
import main

# flaskの設定
app = Flask(__name__)
port = int(os.getenv('VCAP_APP_PORT', 0))


@app.route("/api", methods=['GET'])
def index():
    # url = request.args.get("url")
    # main.start(url)

    response = jsonify({'message': "File is uploaded GoogleDrive"})
    response.status_code = 200
    return response


if __name__ == '__main__':
    app.run(host='herokuapp.com', port=port)
