from pytube import YouTube
import ffmpeg
import os
import shutil
import threading
import src.googledrive as googledrive
import src.uploader as uploader

file_name = ''

ENVIRONMENT_PATH_HEADER = os.getenv('ENVIRONMENT_PATH_HEADER') or os.environ.get('ENVIRONMENT_PATH_HEADER')
TEMP_DIR = ENVIRONMENT_PATH_HEADER + 'tmp/'
CREDENTIALS_PATH = ENVIRONMENT_PATH_HEADER + 'credentials.json'


def get_file_path(name):
    return TEMP_DIR + name


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
    video.download(TEMP_DIR)

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
    if not os.path.exists(CREDENTIALS_PATH):
        print('credentialsなし')
        googledrive.start()
    uploader.start(file_name)

    print("アップロード完了")

    # 要らなくなったので削除
    os.remove(get_file_path(file_name) + '.mp3')


def remake_dir():
    shutil.rmtree(TEMP_DIR)
    os.mkdir(TEMP_DIR)
    print('フォルダのリメイク完了')


# 非同期処理
def thred(url):
    print("非同期処理開始")
    thread = threading.Thread(target=start, args=(url,))
    thread.start()


def start(url):
    print(url)
    remake_dir()

    download(url)
    convert()
    upload()

    remake_dir()
    return '完了'
    # try:
    #     download(url)
    #     convert()
    #     upload()
    #     remake_dir()
    #     return '完了'
    #
    # except:
    #     print('ダメだった')
    #     remake_dir()
    #     return 'もう一度やり直してください'

