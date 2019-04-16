# 参考サイト: http://yura2.hateblo.jp/entry/2016/01/30/Python%E3%81%A7Google_Drive_API_v3%E3%82%92%E5%88%A9%E7%94%A8%E3%81%97%E3%81%A6%E7%94%BB%E5%83%8F%E3%81%AE%E3%82%A2%E3%83%83%E3%83%97%E3%83%AD%E3%83%BC%E3%83%89

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client.file
from oauth2client import client
from oauth2client import tools
from googleapiclient.http import MediaFileUpload

# .envを使うのに必要
from dotenv import load_dotenv

load_dotenv()
load_dotenv(verbose=True)
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# --- end ---

ENVIRONMENT_PATH_HEADER = os.getenv('ENVIRONMENT_PATH_HEADER') or os.environ.get('ENVIRONMENT_PATH_HEADER')
TEMP_DIR = ENVIRONMENT_PATH_HEADER + 'tmp/'
EXTENSION = '.mp3'
MIME_TYPE = 'audio/mp3'
CREDENTIALS_PATH = ENVIRONMENT_PATH_HEADER + 'credentials.json'
FOLDER_ID = os.getenv('folder_id') or os.environ.get('folder_id')
APPLICATION_NAME = 'ConvertMovie2Radio'
SCOPES = os.getenv('scopes') or os.environ.get('scopes')


# ここをコメントアウトするとgunicorn: error: unrecognized argumentsになる
# try:
#     import argparse
#
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None


class GoogleDriveUploader:
    def __init__(self):
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('drive', 'v3', http=self.http)

    def get_credentials(self):
        store = oauth2client.file.Storage(CREDENTIALS_PATH)
        credentials = store.get()
        if not credentials or credentials.invalid:
            # セーブしないのでflow_from_clientsecretsのfilenameはいらない
            flow = client.flow_from_clientsecrets('', SCOPES)
            flow.user_agent = APPLICATION_NAME

            credentials = tools.run(flow, store)
            print('Storing credentials to ' + CREDENTIALS_PATH)
        return credentials

    def upload_file(self, file_name):
        # ファイルをアップロードする
        file_path = TEMP_DIR + file_name + EXTENSION
        media_body = MediaFileUpload(file_path, mimetype=MIME_TYPE, resumable=True)
        body = {
            'name': file_name,
            'mimeType': MIME_TYPE,
            'parents': [FOLDER_ID],
        }
        self.service.files().create(body=body, media_body=media_body).execute()


def start(file_name):
    uploader = GoogleDriveUploader()
    uploader.upload_file(file_name)

# if __name__ == '__main__':
#     uploader = GoogleDriveUploader()
#     uploader.upload_file('hoge')
