import os
from pytube import YouTube


class Downloader:

    def __init__(self, url):
        self.yt = YouTube(url)
        self.videoTitle = self.yt.title
        self.getStream()

    def getStream(self):
        print('\n[Title] {0}\n'.format(self.videoTitle))

        st = self.yt.streams
        self.showList(st.filter(adaptive=True, only_video=True, subtype="mp4"))
        itag_v = self.selectStream("Video")

        self.showList(st.filter(adaptive=True, only_audio=True))
        itag_a = self.selectStream("Audio")

        self.yt.register_on_progress_callback(self.progress)

        root, self.ext_v = os.path.splitext(st.get_by_itag(itag_v).default_filename)
        root, self.ext_a = os.path.splitext(st.get_by_itag(itag_a).default_filename)

        st.get_by_itag(itag_v).download("", "tmp_Video")
        st.get_by_itag(itag_a).download("", "tmp_Audio")

    def showList(self, list):
        for i in list.all():
            print(i)

    def selectStream(self, fileType):
        while True:
            itag = int(input("Select " + fileType + " itag#: "))
            if self.yt.streams.get_by_itag(itag) != None:
                break
        return itag

    def progress(self, stream, chunk, file_handle, bytes_remaining):
        p = round(file_handle.tell() / (file_handle.tell() + bytes_remaining) * 100, 1)
        print(file_handle, p, "%")


class Converter:

    def __init__(self, filename, vext, aext):
        self.filename = filename
        self.videoExt = vext
        self.audioExt = aext
        self.convert()

    def convert(self):
        convcmd = "ffmpeg -i {} -i {} -y -vcodec copy {}".format("tmp_Video" + self.videoExt,
                                                                 "tmp_Audio" + self.audioExt,
                                                                 "\"" + self.filename + "\"" + ".mp4")

        os.system(convcmd)

        self.deleteFile(self.delete, "Video")
        self.deleteFile(self.delete, "Audio")

    def deleteFile(self, function, fileType):
        q = input("Delete " + fileType + "-Only-File? y/n : ")
        if q == "y":
            function(fileType)

    def delete(self, f):
        if f == "Video":
            target = "tmp_Video" + self.videoExt
        elif f == "Audio":
            target = "tmp_Audio" + self.audioExt

        os.system("del " + target)


if __name__ == "__main__":
    url = input("Enter YouTube Video URL : ")
    d = Downloader(url)
    c = Converter(d.videoTitle, d.ext_v, d.ext_a)
