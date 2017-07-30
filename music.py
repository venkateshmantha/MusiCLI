import os,random,sys
import pygame

SONG_END = pygame.USEREVENT + 1
pygame.mixer.init()

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

    while songs:
        play_songs(songs)

    print("Queue is empty!")

def play_songs(songs):

    curr_song = random.choice(songs)
    #print("Now playing: " + curr_song)
    pygame.mixer.music.load(curr_song)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(100)

    pygame.mixer.music.set_endevent(SONG_END)

    if pygame.mixer.music.get_endevent() == SONG_END:
        songs.remove(curr_song)


if __name__ == '__main__':
    init()
