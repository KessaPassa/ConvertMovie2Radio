from pytube import YouTube
import ffmpeg
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import threading
import urllib.request as request
import oauth2client.client
import httplib2
import json

file_name = ""


def download(url):
    yt = YouTube(url)

    # 特殊文字が入っていると消されて、ファイルのパスを取得できないので
    global file_name
    file_name = yt.title
    list = ["　", "/", ":", "*", "?", "<", ">", "|", "\"", "\\", "\'", "."]
    for item in list:
        file_name = file_name.replace(item, "")
    # タイトルを変更
    yt.player_config_args["title"] = file_name

    video = yt.streams.filter(progressive=True, file_extension='mp4').first()
    video.download()

    print(file_name, "のダウンロード完了")


def convert():
    mp4 = file_name + ".mp4"
    mp3 = file_name + ".mp3"
    stream = ffmpeg.input(mp4)
    stream = ffmpeg.output(stream, mp3)
    ffmpeg.run(stream)
    print("コンバート完了")

    # 要らなくなったので削除
    os.remove(mp4)


def upload():
    gauth = GoogleAuth()

    credentials_file = 'credentials.json'
    client_id = ''
    client_secret = ''
    access_token = ''
    scope = ''

    if os.path.exists(credentials_file):
        with open(credentials_file) as f:
            print('ファイル読み込み')
            cred_dir = json.load(f)

            client_id = cred_dir['client_id']
            client_secret = cred_dir['client_secret']
            access_token = cred_dir['access_token']
            scope = cred_dir['scopes'][1]

            # print(cred_dir['access_token'])
            # code = oauth2client.client.AccessTokenCredentials(cred_dir['access_token'], 'my-user-agent/1.0')

    else:
        print('環境変数読み込み')
        client_id = os.environ.get('client_id')
        client_secret = os.environ.get('client_secret')
        access_token = os.environ.get('access_token')

    flow = oauth2client.client.OAuth2WebServerFlow(client_id, client_secret,
                                                   scope=scope,
                                                   redirect_uri='http://127.0.0.1:8000')

    flow.step1_get_authorize_url()
    # print(auth_uri)
    flow_info = flow.step1_get_device_and_user_codes()
    print(flow_info)
    code = flow_info.device_code
    # step2 = flow.step2_exchange(device_flow_info=flow_info)
    # print(step2)

    credentials = flow.step2_exchange(device_flow_info=flow_info)
    # credentials = oauth2client.client.credentials_from_code(client_id, client_secret,
    #                                                         scope=scope,
    # #                                                         code=code)
    credentials.authorize(httplib2.Http())
    gauth.credentials = credentials

    # gauth = GoogleAuth()
    # oauth_url = gauth.GetAuthUrl()
    # # print(oauth_url)
    #
    # req = request.Request(oauth_url)
    # with request.urlopen(req) as res:
    #     body = res.read()
    #     print(body.decode('utf-8'))
    #     # f = open('text.txt', 'w')
    #     # f.write(body.decode('utf-8'))
    #     # f.close()

    # Try to load saved client credentials
    # print('1')
    # gauth.LoadCredentialsFile(save_file)
    # if gauth.credentials is None:
    #     print('2')
    #     # Authenticate if they're not there
    #     gauth.LocalWebserverAuth()
    # elif gauth.access_token_expired:
    #     print('3')
    #     # Refresh them if expired
    #     gauth.Refresh()
    # else:
    #     print('4')
    #     # Initialize the saved creds
    #     gauth.Authorize()
    #
    # # Save the current credentials to a file
    # print('5')
    # gauth.SaveCredentialsFile(save_file)
    # drive = GoogleDrive(gauth)
    #
    # file_name = '26【8曲】MYTH&ROIDアニソンメドレー Anime songs medley'
    # mp3 = file_name + ".mp3"
    # folder_id = '1iopccLVKuBrYRZx8hnfXGsvNrLTZpB1b'
    # metadata = {
    #     'parents': [{"kind": "drive#fileLink", "id": folder_id}]
    # }
    #
    # f = drive.CreateFile(metadata)
    # f.SetContentFile(mp3)
    # f.Upload()
    # print("アップロード完了")

    # 要らなくなったので削除
    # os.remove(mp3)


# 非同期処理
def thred(url):
    print("非同期処理開始")
    thread = threading.Thread(target=start, args=(url,))
    thread.start()


def start(url):
    print(url)
    upload()
    # try:
    #     download(url)
    #     convert()
    #     upload()
    #
    # except:
    #     print('ダメだった')
