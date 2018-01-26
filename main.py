# -*- coding: utf-8 -*-
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
    video.download()

    #特殊文字が入っていると消されて、ファイルのパスを取得できないので
    global fileTitle
    fileTitle = yt.title
    list = ["/", ":", "*", "?", "<", ">", "|"]
    for item in list:
        fileTitle = fileTitle.replace(item, "")
    global folderPath
    folderPath = fileTitle
    print(fileTitle, "のダウンロード完了")


def convert():
    mp4 = folderPath + ".mp4"
    mp3 = folderPath + ".mp3"

    stream = ffmpeg.input(mp4)
    stream = ffmpeg.output(stream, mp3)
    ffmpeg.run(stream)
    print("コンバート完了")

    # 要らなくなったので削除
    os.remove(mp4)


def upload():
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)

    mp3 = folderPath + ".mp3"
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


#非同期処理
async def start(url):
    pass

    download(url)
    convert()
    upload()
