from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


def upload(name):
    name += ".mp3"
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

    #要らなくなったので削除
    os.remove(name)
