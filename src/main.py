from pytube import YouTube
import ffmpeg
import os
import threading
import src.googledrive as googledrive
import src.uploader as uploader

file_name = ''
FOLDER_DIR = './tmp/'


def get_file_path(name):
    return FOLDER_DIR + name


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
    video.download(FOLDER_DIR)

    print(file_name, "のダウンロード完了")


def convert():
    mp4 = get_file_path(file_name) + ".mp4"
    mp3 = get_file_path(file_name) + ".mp3"
    stream = ffmpeg.input(mp4)
    stream = ffmpeg.output(stream, mp3)
    ffmpeg.run(stream)
    print("コンバート完了")

    # 要らなくなったので削除
    os.remove(mp4)


def upload():
    if not os.path.exists('credentials.json'):
        googledrive.start()
    uploader.start(file_name)

    print("アップロード完了")

    # 要らなくなったので削除
    os.remove(get_file_path(file_name)+'.mp3')


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
        upload()
    except:
        print('ダメだった')
