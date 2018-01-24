from pytube import YouTube
import ffmpeg
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

fileTitle = ""

def download():
    url = input("URL>")
    yt = YouTube(url)
    video = yt.streams.filter().first()
    video.download()
    print(yt.title, "のダウンロード完了")

    global fileTitle
    fileTitle = yt.title


def convert():
    stream = ffmpeg.input(fileTitle + ".mp4")
    stream = ffmpeg.output(stream, fileTitle + ".mp3")
    ffmpeg.run(stream)
    print("コンバート完了")

    # 要らなくなったので削除
    os.remove(fileTitle + ".mp4")


def upload():
    name = fileTitle + ".mp3"
    print(name)
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)

    folder_id = '1iopccLVKuBrYRZx8hnfXGsvNrLTZpB1b'
    metadata = {
        'title': name,
        'parents': [{"kind": "drive#fileLink", "id": folder_id}]
    }
    f = drive.CreateFile(metadata)
    f.SetContentFile(name)
    f.Upload()
    print("アップロード完了")

    # 要らなくなったので削除
    os.remove(name)


if __name__ == '__main__':
    download()
    convert()
    upload()
