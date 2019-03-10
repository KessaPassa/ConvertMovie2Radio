# -*- coding: utf-8 -*-
# from browser import document, alert
from flask import jsonify
import threading
import main


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

# def submit(event):
#     url = document['url_field'].value
#     alert(url)
#     # main.start(url)
#     document['url_field'].value = ''
#
#
# document['submit_url'].bind('click', submit)
