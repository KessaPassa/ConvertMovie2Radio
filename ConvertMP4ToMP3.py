import ffmpeg
import os

def convert(filename):
    # filename = input("ファイルの名前> ")
    split = filename.split(".")

    rowFilename = ""
    if len(split) == 1:
        rowFilename = split[0]
    else:
        for i in range(len(split) - 1):
            rowFilename += split[i]
    print(rowFilename)

    stream = ffmpeg.input(rowFilename+".mp4")
    stream = ffmpeg.output(stream, rowFilename + ".mp3")
    ffmpeg.run(stream)

    #要らなくなったので削除
    os.remove(rowFilename+".mp4")