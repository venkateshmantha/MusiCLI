import os, pygame, mutagen.mp3
from tkinter.filedialog import askdirectory
from tkinter import *
from tkinter import messagebox

root = Tk()
root.wm_title("MusiCLI")
index = 0
count = 0
pause = True

topframe = Frame(root)
topframe.pack()
bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)

label = Label(topframe, text="Jukebox")
label.pack()

listbox = Listbox(topframe, width=80)
listbox.pack(fill=X, side=BOTTOM)

songs = []

v = StringVar()
songlabel = Label(bottomframe, textvariable=v, width=80)
songlabel.pack()

openbutton = Button(bottomframe, text="Open")
openbutton.pack(side=LEFT, ipadx=25)

previousbutton = Button(bottomframe, text="Prev")
previousbutton.pack(side=LEFT, ipadx=30)

playbutton = Button(bottomframe, text="Play")
playbutton.pack(side=LEFT, ipadx=30)

stopbutton = Button(bottomframe, text="Stop")
stopbutton.pack(side=LEFT, ipadx=30)

nextbutton = Button(bottomframe, text="Next")
nextbutton.pack(side=LEFT, ipadx=30)

pausebutton = Button(bottomframe, text="Pause")
pausebutton.pack(side=LEFT, ipadx=30)


def updatelabel():
    global index
    v.set(songs[index])


def pausesong(event):
    global pause

    if pause:
        pygame.mixer.music.pause()
        pause = False
    else:
        pygame.mixer.music.unpause()


def playsong(event):
    pygame.mixer.music.play()


def nextsong(event):
    global index
    index += 1
    if index < count:
        pygame.mixer.music.load(songs[index])
        pygame.mixer.music.play()
    else:
        index = 0
        pygame.mixer.music.load(songs[index])
        pygame.mixer.music.play()
    try:
        updatelabel()
    except NameError:
        print("")


def previoussong(event):
    global index
    index -= 1
    pygame.mixer.music.load(songs[index])
    pygame.mixer.music.play()
    try:
        updatelabel()
    except NameError:
        print("")


def stopsong(event):
    pygame.mixer.music.stop()


def directorychooser():
    global count
    global index

    directory = askdirectory()

    if directory:
        count = 0
        index = 0

        del songs[:]
        os.chdir(directory)

        for file in os.listdir(directory):
            if file.endswith(".mp3"):
                songs.append(file)

        if len(songs) == 0:
            retry = messagebox.askretrycancel("No songs found", "No songs found!")
            if retry:
                directorychooser()

        else:
            listbox.delete(0, END)
            for song in songs:
                listbox.insert(END, song)
                count += 1

            file = mutagen.mp3.MP3(songs[0])
            pygame.mixer.init(frequency=file.info.sample_rate)
            pygame.mixer.music.load(songs[0])
            pygame.mixer.music.play()
            try:
                updatelabel()
            except NameError:
                print("")
    else:
        return 1


def choosedirectory(event):
    try:
        directorychooser()
    except WindowsError:
        print("Exiting!")


openbutton.bind("<Button-1>", choosedirectory)
playbutton.bind("<Button-1>", playsong)
nextbutton.bind("<Button-1>", nextsong)
previousbutton.bind("<Button-1>", previoussong)
stopbutton.bind("<Button-1>", stopsong)
pausebutton.bind("<Button-1>", pausesong)

try:
    directorychooser()
except:
    print("Exited!")

root.mainloop()
