from pytube import YouTube
import ffmpeg
import os
import shutil
import threading
import src.googledrive as googledrive
import src.uploader as uploader

file_name = ''
DIR_NAME = './tmp/'


def get_file_path(name):
    return DIR_NAME + name


def download(url):
    print(1)
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
    video.download(DIR_NAME)

    print(file_name, "のダウンロード完了")


def convert():
    print(2)
    mp4 = get_file_path(file_name) + ".mp4"
    mp3 = get_file_path(file_name) + ".mp3"
    stream = ffmpeg.input(mp4)
    stream = ffmpeg.output(stream, mp3)
    ffmpeg.run(stream)
    print("コンバート完了")

    # 要らなくなったので削除
    os.remove(mp4)


def upload():
    print(3)
    if not os.path.exists('credentials.json'):
        googledrive.start()
    uploader.start(file_name)

    print("アップロード完了")

    # 要らなくなったので削除
    os.remove(get_file_path(file_name) + '.mp3')


def remake_dir():
    shutil.rmtree(DIR_NAME)
    os.mkdir(DIR_NAME)
    print('フォルダのリメイク完了')


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
        remake_dir()
        return '完了'

    except:
        print('ダメだった')
        return 'もう一度やり直してください'
