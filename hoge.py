from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

if __name__ == '__main__':
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file_name = '26【8曲】MYTH&ROIDアニソンメドレー Anime songs medley'
    mp3 = file_name + ".mp3"
    folder_id = '1iopccLVKuBrYRZx8hnfXGsvNrLTZpB1b'
    metadata = {
        'parents': [{"kind": "drive#fileLink", "id": folder_id}]
    }

    f = drive.CreateFile(metadata)
    f.SetContentFile(mp3)
    f.Upload()
    print("アップロード完了")

'https://accounts.google.com/o/oauth2/auth' \
'?client_id=254274857640-m67daekujrusm6gpnlf9ud8o7tdmif03.apps.googleusercontent.com' \
'&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F' \
'&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.file+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.install' \
'&access_type=offline' \
'&response_type=code' \
'&approval_prompt=force'


