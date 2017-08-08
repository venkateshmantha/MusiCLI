import os, pygame, mutagen.mp3
from tkinter.filedialog import askdirectory
from tkinter import *
from tkinter import messagebox

# Tkinter window init
root = Tk()

# Setting transparency of the window
root.attributes('-alpha', 0.9)

bgcolor = "#191a1c"
fgcolor = "#14a001"

root.configure(bg=bgcolor)
root.wm_title("MusiCLI")

# Global variables
index = 0
count = 0
pause = True
songs = []

# Frames init
topframe = Frame(root)
topframe.configure(bg=bgcolor)
topframe.pack(fill=X)

midframe = Frame(root, height=10, width=80)
midframe.configure(bg=bgcolor)
midframe.pack()

bottomframe = Frame(root, height=15, width=80)
bottomframe.configure(bg=bgcolor)
bottomframe.pack()

listbox = Listbox(topframe, width=100)
listbox.configure(bg=bgcolor, fg=fgcolor)
listbox.pack(fill=X)

v = StringVar()
songlabel = Label(midframe, textvariable=v, width=80)
songlabel.configure(bg=bgcolor, fg=fgcolor)
songlabel.pack()

# Buttons init
openbutton = Button(midframe, text="Open")
openbutton.configure(bg=bgcolor, fg=fgcolor)
openbutton.pack(side=LEFT, ipadx=50)

previousbutton = Button(midframe, text="Prev")
previousbutton.configure(bg=bgcolor, fg=fgcolor)
previousbutton.pack(side=LEFT, ipadx=50)

pausebutton = Button(midframe, text="Play/Pause")
pausebutton.configure(bg=bgcolor, fg=fgcolor)
pausebutton.pack(side=LEFT, ipadx=50)

nextbutton = Button(midframe, text="Next")
nextbutton.configure(bg=bgcolor, fg=fgcolor)
nextbutton.pack(side=LEFT, ipadx=50)


# Functions
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

    # Opening Windows dialog
    directory = askdirectory()

    if directory:
        count = 0
        index = 0

        # Empty the previous list
        del songs[:]

        # Reset pause
        global pause
        pause = True

        os.chdir(directory)

        for file in os.listdir(directory):
            if file.endswith(".mp3"):
                songs.append(file)

        if len(songs) == 0:
            # Windows dialog to retry in the event of no mp3 files
            retry = messagebox.askretrycancel("No songs found", "No songs found!")
            if retry:
                directorychooser()

        else:
            # Clear the listbox
            listbox.delete(0, END)
            for song in songs:
                listbox.insert(END, song)
                count += 1

            # Using the mutagen library to extract the sample rate of the mp3 file
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

# Function to choose a different playback directory
def choosedirectory(event):
    try:
        directorychooser()
    except WindowsError:
        print("Exiting!")

# TODO
# def playall():

# Binding widgets to functions
openbutton.bind("<Button-1>", choosedirectory)
nextbutton.bind("<Button-1>", nextsong)
previousbutton.bind("<Button-1>", previoussong)
pausebutton.bind("<Button-1>", pausesong)

# Program init
try:
    directorychooser()
except:
    print("Exited!")

root.mainloop()
