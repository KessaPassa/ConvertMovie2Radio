from pytube import YouTube
import ffmpeg
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

fileTitle = ""
folderPath = ""

def download(url):
    yt = YouTube(url)
    video = yt.streams.filter(file_extension='mp4').first()
    video.download("/tmp")

    #特殊文字が入っていると消されて、ファイルのパスを取得できないので
    global fileTitle
    fileTitle = yt.title
    list = ["/", ":", "*", "?", "<", ">", "|"]
    for item in list:
        fileTitle = fileTitle.replace(item, "")
    global folderPath
    folderPath = "/tmp/" + fileTitle
    print(fileTitle, "のダウンロード完了")
    print(folderPath)


def convert():
    stream = ffmpeg.input(folderPath + ".mp4")
    stream = ffmpeg.output(stream, folderPath + ".mp3")
    ffmpeg.run(stream)
    print("コンバート完了")

    # 要らなくなったので削除
    os.remove(folderPath + ".mp4")


def upload():
    print(folderPath)
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)

    folder_id = '1iopccLVKuBrYRZx8hnfXGsvNrLTZpB1b'
    metadata = {
        'title': fileTitle + ".mp4",
        'parents': [{"kind": "drive#fileLink", "id": folder_id}]
    }
    f = drive.CreateFile(metadata)
    f.SetContentFile(folderPath + ".mp4")
    f.Upload()
    print("アップロード完了")

    # 要らなくなったので削除
    os.remove(folderPath+".mp3")


def start(url):
    download(url)
    # convert()
    upload()
