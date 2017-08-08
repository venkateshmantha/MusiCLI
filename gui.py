import os, pygame, mutagen.mp3
from tkinter.filedialog import askdirectory
from tkinter import *
from tkinter import messagebox

root = Tk()
root.attributes('-alpha', 0.9)
root.configure(bg="#191a1c")
root.wm_title("MusiCLI")
index = 0
count = 0
pause = True

topframe = Frame(root)
topframe.configure(bg="#191a1c")
topframe.pack(fill=X)

midframe = Frame(root, height=10, width=80)
midframe.configure(bg="#191a1c")
midframe.pack()

bottomframe = Frame(root, height=15, width=80)
bottomframe.configure(bg="#191a1c")
bottomframe.pack()

listbox = Listbox(topframe, width=100)
listbox.configure(bg="#191a1c", fg="#14a001")
listbox.pack(fill=X)

songs = []

v = StringVar()
songlabel = Label(midframe, textvariable=v, width=80)
songlabel.configure(bg="#191a1c", fg="#14a001")
songlabel.pack()

openbutton = Button(midframe, text="Open")
openbutton.configure(bg="#191a1c", fg="#14a001")
openbutton.pack(side=LEFT, ipadx=50)

previousbutton = Button(midframe, text="Prev")
previousbutton.configure(bg="#191a1c", fg="#14a001")
previousbutton.pack(side=LEFT, ipadx=50)

pausebutton = Button(midframe, text="Play/Pause")
pausebutton.configure(bg="#191a1c", fg="#14a001")
pausebutton.pack(side=LEFT, ipadx=50)

nextbutton = Button(midframe, text="Next")
nextbutton.configure(bg="#191a1c", fg="#14a001")
nextbutton.pack(side=LEFT, ipadx=50)


def updatelabel():
    global index
    v.set("Now playing: " + songs[index])


def pausesong(event):
    global pause

    if pause:
        pygame.mixer.music.pause()
        pause = False
    else:
        pygame.mixer.music.unpause()


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


def directorychooser():
    global count
    global index

    directory = askdirectory()

    if directory:
        count = 0
        index = 0

        del songs[:]
        global pause
        pause = True
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
nextbutton.bind("<Button-1>", nextsong)
previousbutton.bind("<Button-1>", previoussong)
pausebutton.bind("<Button-1>", pausesong)

try:
    directorychooser()
except:
    print("Exited!")

root.mainloop()
