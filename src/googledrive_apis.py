import urllib.request
import json
import base64

base_url = 'https://www.googleapis.com/'
api_key = 'AIzaSyBboQXtoSdPUaKwBPBbr0up03t4C2rLH_U'
folder_id = '1iopccLVKuBrYRZx8hnfXGsvNrLTZpB1b'


def upload(access_token):
    url = base_url + 'drive/v3/files' + '?uploadType=multipart'#'?uploadType=resumable'
    file = open('hoge.mp3', 'rb').read()
    file = base64.b64encode(file).decode('utf-8')
    with open('base64.txt', 'w') as f:
        f.write(file)
    print(type(file))

    data = {
        'file': file,
        'parents': [
            folder_id,
        ],
        'name': 'hoge.mp3',
        'mimeType': 'audio/mp3',
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method='POST')
    with urllib.request.urlopen(req) as res:
        body = json.loads(res.read())
        print(body)
