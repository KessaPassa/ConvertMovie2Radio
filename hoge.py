import os

if __name__ == "__main__":
    file_name = '/Users/kessapassa/Documents/github/ConvertMovie2Radio/26【8曲】MYTH&ROIDアニソンメドレー Anime songs medley'
    convert_cmd = 'ffmpeg -i {}.mp4 {}.mp3'.format(file_name, file_name)
    os.system(convert_cmd)