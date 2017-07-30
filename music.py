import os,random,sys
from pygame import *

def init():

    directory = sys.argv[1]
    songs = []
    os.chdir(directory)
    for root, folders, files in os.walk(directory):
        folders.sort()
        files.sort()
        for file in files:
            if file.endswith(".mp3"):
                songs.append(os.path.join(root, file))
    playsongs(songs)

def playsongs(songs):

    random.shuffle(songs)
    mixer.init()
    mixer.music.load(songs[0])
    mixer.music.play(0)
    for song in songs:
        mixer.music.queue(song)

    while mixer.music.get_busy():
        time.Clock().tick(100)


if __name__ == '__main__':
    init()