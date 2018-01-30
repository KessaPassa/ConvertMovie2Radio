# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import main
import os
import threading

# flaskの設定
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/api", methods=['GET'])
def get():
    print("getメソッドです")
    url = request.args.get("url")
    return start(url)


@app.route("/api", methods=['POST'])
def post():
    print("postメソッドです")
    url = request.form["url"]
    return start(url)


def start(url):
    response = ""
    print(url)
    if not (url is None):
        thread = threading.Thread(target=main.start, args=(url,))
        thread.start()

        print("非同期処理開始")
        response = jsonify({'message': "File is uploaded GoogleDrive"})
        response.status_code = 200

    else:
        response = jsonify({'message': "You must append '/api?url=Youtube_URL'"})
        response.status_code = 404

    return response



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
