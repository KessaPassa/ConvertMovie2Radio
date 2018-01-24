from pytube import YouTube

def download():
    url = input("URL>")
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    video.download()
    print(yt.title, "のダウンロード完了")
    return yt.title