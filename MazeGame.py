import os
from textwrap import fill
import tkinter as tk
from DifferentMaze import DifferentMaze
from HomeScreen import HomeScreen
from NewGame import NewGame
from LoadGame import LoadGame
import pygame
from PIL import ImageTk, Image
from threading import Thread

class MazeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MazeRider 1.0")
        self.my_sound = None
        self.my_music = None
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('%dx%d+0+0' % (self.width, self.height))
        self.state("zoomed")
        self.update_idletasks()
        self.width, self.height = self.winfo_width(), self.winfo_height()
        self.attributes("-fullscreen", False)
        #self.attributes('-zoomed', True)
        self.resizable(True, True)
        self.container = tk.Frame(self, bg='#d0c4b4')
        self.container.pack(side="top", fill="both", expand="True")
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
        self.directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.frames = {"DifferentMaze": DifferentMaze, "HomeScreen": HomeScreen, "NewGame": NewGame, "LoadGame": LoadGame}
        self.visibleFrame = None
        self.bind("<F11>", self.fullScreen(True))
        self.bind("<Escape>", self.fullScreen(False))
        self.playsound(file = self.getPath('HSSound.mp3'))
        self.show_frame('HomeScreen')

    def show_frame(self, classname, *args, **kwargs):
        if self.visibleFrame!=None:
            self.visibleFrame.destroy()
            del(self.visibleFrame)
        if(len(args)!=0):
            self.visibleFrame = self.frames[classname](self, self.container, *args, **kwargs)
        else:
            self.visibleFrame = self.frames[classname](self, self.container)
        self.visibleFrame.grid(row = 0, column = 0, sticky = "nsew")
        if(classname == 'HomeScreen'):
            self.menu = self.visibleFrame.createMenubar(self)
            self.configure(menu = self.menu)
        self.visibleFrame.tkraise()
        self.visibleFrame.focus_set()
        if(classname == 'DifferentMaze'):
            self.visibleFrame.startGhost(self)

    def playsound(self, file):
        if pygame.mixer.get_init()!=None:
            pygame.mixer.quit()
        pygame.mixer.init()
        self.my_sound = pygame.mixer
        self.my_music = self.my_sound.music
        self.my_music.load(file)
        self.my_music.play(loops=-1)
        self.my_music.set_volume(0.3)

    def stopsound(self, flag):
        if flag==True:
            self.my_music.pause()
        else:
            self.my_music.unpause()

    def flicksound(self):
        if self.my_music.get_busy()==True:
            self.my_music.pause()
        else:
            self.my_music.unpause()

    def setvolume(self, value):
        self.my_music.set_volume(value)

    def setmusic(self, value):
        self.my_music.set_pos(value)

    def getPath(self, file):
        return os.path.join(self.directory, file)

    def resizer(self, path, canvas, item, width, height):
        t = Thread(target = self.resizerFunction(path, canvas, item, width, height))
        t.start()
      
    def resizerFunction(self, path, canvas, item, width, height):
        image = Image.open(path)
        resized = image.resize((width, height), Image.ANTIALIAS)
        setattr(self, str(canvas)+str(item), ImageTk.PhotoImage(resized))
        canvas.itemconfigure(item, image=getattr(self, str(canvas)+str(item)))
        if(canvas.find_withtag('background')):
            if(item == canvas.find_withtag('background')[0]):
                for widget in canvas.find_withtag('button'):
                    canvas.move(widget, canvas.coords(widget)[0]*((width/self.width)-1), canvas.coords(widget)[1]*((height/self.height)-1))

                for widget in canvas.find_withtag('text'):
                    canvas.move(widget, canvas.coords(widget)[0]*((width/self.width)-1), canvas.coords(widget)[1]*((height/self.height)-1))

                self.width = width
                self.height = height

    def toolbar(self, canvas):
        self.ng_path = "unmute.png"
        self.NG_image = tk.PhotoImage(file = self.getPath(self.ng_path))
        self.ngimg = canvas.create_image(self.winfo_width(),0, image= self.NG_image, anchor = 'ne', tag="button")
 
        self.NGP_image = tk.PhotoImage(file = self.getPath("unmute.png"))
        canvas.tag_bind(self.ngimg, "<Button-1>", lambda event: volume(), add="+")
        canvas.tag_bind(self.ngimg, "<Button-1>", lambda event: self.resizer(self.getPath(self.ng_path), canvas, self.ngimg, int(self.winfo_width()*0.08), int(self.winfo_height()*0.08)), add="+")
        canvas.tag_bind(self.ngimg, "<Button-1>", lambda event: self.flicksound(), add="+")

        self.max_path = "maximize.png"
        self.MAX_image = tk.PhotoImage(file = self.getPath(self.max_path))
        self.maximg = canvas.create_image(self.winfo_width(),self.winfo_height()*0.09, image= self.MAX_image, anchor = 'ne', tag="button")
 
        self.MAXP_image = tk.PhotoImage(file = self.getPath("minimize.png"))
        canvas.tag_bind(self.maximg, "<Button-1>", lambda event: fullScreen(), add="+")
        canvas.tag_bind(self.maximg, "<Button-1>", lambda event: self.resizer(self.getPath(self.max_path), canvas, self.maximg, int(self.winfo_width()*0.08), int(self.winfo_height()*0.08)), add="+")

        canvas.bind('<Configure>', lambda event: resizeWin(event))
        def resizeWin(event, *args):
            flag = args[0] if len(args)!=0 else False
            if(flag or ((self.width, self.height) != (event.width, event.height))):
                self.resizer(self.getPath(self.ng_path), canvas, self.ngimg, int(self.winfo_width()*0.08), int(self.winfo_height()*0.08))
                self.resizer(self.getPath(self.max_path), canvas, self.maximg, int(self.winfo_width()*0.08), int(self.winfo_height()*0.08))
    
        resizeWin(None, True)

        def volume():
            print(self.my_music.get_busy())
            if(self.my_music.get_busy()==True):
                setattr(self, 'ng_path', "mute.png")
            else:
                 setattr(self, 'ng_path', "unmute.png")

        def fullScreen():
            print(self.attributes('-fullscreen'))
            if(self.attributes('-fullscreen')==True):
                setattr(self, 'max_path', "minimize.png")
                self.fullScreen(False)
            else:
                 setattr(self, 'max_path', "maximize.png")
                 self.fullScreen(True)
    
    def quit(self):
        self.destroy()
    
    def addMenuBar(self, newMenu):
        self.menu.add_cascade(label="Menu", menu=newMenu)

    def deleteMenuBar(self, label):
        self.menu.delete(label)

    def fullScreen(self, value):
        self.attributes("-fullscreen", value)

    def showOptions(self):
        options = tk.Toplevel()
        options.geometry("%dx%d%+d%+d" % (self.winfo_width()/3, self.winfo_height()/3, self.winfo_width()/2, self.winfo_height()/2))
        options.title('Options')
        options.grid_columnconfigure(0, weight=1)
        options.grid_columnconfigure(1, weight=1)
        options.grid_rowconfigure(0, weight=1)
        options.grid_rowconfigure(1, weight=1)
        options.grid_rowconfigure(2, weight=1)
        options.grid_rowconfigure(3, weight=1)
        label = tk.Label(options, text="Toggle Fullscreen", font=("terminal 12"), justify=tk.LEFT)
        label.grid(row=0, column=0)
        full_state = tk.BooleanVar()
        full = tk.Checkbutton(options, text='ticked = true', var = full_state, command=lambda: self.fullScreen(full_state.get()))
        full.grid(row=0,column=1)

        labelS = tk.Label(options, text="Volume control", font=("terminal 12"), justify=tk.LEFT)
        labelS.grid(row=1, column=0)
        self.volumeS = tk.Scale(options)
        self.volume = tk.IntVar(value=0)
        self.volumeS.configure(
            cursor="cross", from_="0", length="170", orient="horizontal",
            state="normal", to="100", variable=self.volume, tickinterval=20, font='terminal 12',
            command = lambda value: self.setvolume(self.volume.get())
        )
        self.volumeS.grid(column="1", row="1", sticky="ne")

        labelP = tk.Label(options, text="Pause music", font=("terminal 12"), justify=tk.LEFT)
        labelP.grid(row=2, column=0)
        paused = tk.BooleanVar()
        pause = tk.Checkbutton(options, text='ticked = pause', var = paused, command=lambda: self.stopsound(paused.get()))
        pause.grid(row=2,column=1)

        labelPos = tk.Label(options, text="Rewind music", font=("terminal 12"), justify=tk.LEFT)
        labelPos.grid(row=3, column=0)
        self.posS = tk.Scale(options)
        self.pos = tk.IntVar(value=0)
        self.posS.configure(
            cursor="cross", from_="0", length="170", orient="horizontal",
            state="normal", to="1000", variable=self.pos, tickinterval=1000, font='terminal 12',
            command = lambda value: self.setmusic(self.pos.get())
        )
        self.posS.grid(column="1", row="3", sticky="ne")
        

if __name__ == '__main__':
    mazeGame = MazeGame()
    mazeGame.mainloop()