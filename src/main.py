from pytube import YouTube
import ffmpeg
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import threading

file_name = ""


def download(url):
    yt = YouTube(url)
    print('おけ')

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
    print(file_name)
    convert_cmd = 'ffmpeg -i {}.mp4 {}.mp3'.format(file_name, file_name)
    os.system(convert_cmd)
    print('コマンドコンバート成功')

    # mp4 = fileTitle + ".mp4"
    # mp3 = fileTitle + ".mp3"
    # print('1')
    # stream = ffmpeg.input(mp4)
    # print('2')
    # stream = ffmpeg.output(stream, mp3)
    # print('3')
    # ffmpeg.run(stream)
    # print("コンバート完了")
    #
    # # 要らなくなったので削除
    # os.remove(mp4)


def upload():
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)

    mp3 = file_name + ".mp3"
    folder_id = '1iopccLVKuBrYRZx8hnfXGsvNrLTZpB1b'
    metadata = {
        'parents': [{"kind": "drive#fileLink", "id": folder_id}]
    }
    f = drive.CreateFile(metadata)
    f.SetContentFile(mp3)
    f.Upload()
    print("アップロード完了")

    # 要らなくなったので削除
    os.remove(mp3)


# 非同期処理
def thred(url):
    print("非同期処理開始")
    thread = threading.Thread(target=start, args=(url,))
    thread.start()


def start(url):
    print(url)

    try:
        download(url)
        convert()
        # upload()

    except:
        print('ダメだった')
