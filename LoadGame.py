from configparser import ConfigParser
from dataclasses import dataclass
from datetime import date
import os
from threading import Thread
import tkinter as tk
from tkinter import Y, StringVar, ttk
from turtle import bgcolor
from PIL import ImageTk, Image

class LoadGame(tk.Frame):
    def __init__(self, master, container):
        super().__init__(container)
        self.pack(fill=tk.BOTH, expand=1)
        master.update_idletasks()

        canvas = tk.Canvas(self)
        canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        scrollbar = ttk.Scrollbar(canvas, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set,yscrollincrement=100)
        canvas.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')), add="+")
        self.toLoad = ""
        self.buttons = []
        secondFrame = tk.Canvas(canvas, bd=0, highlightthickness=1, highlightbackground="black", height=canvas.winfo_height())
        secondFrame.grid_columnconfigure(0, weight=1)
        secondFrame.grid_columnconfigure(1, weight=1)
        secondFrame.grid_columnconfigure(2, weight=1)
        secondFrame.grid_rowconfigure(0, weight=1)

        window = canvas.create_window((master.winfo_width()/2,0), window=secondFrame, anchor="n")
        canvas.itemconfig(window, width = master.winfo_width()/2)
        canvas.bind('<Configure>', lambda event:(secondFrame.winfo_width()) != (event.width) if canvas.itemconfig(window, width = canvas.winfo_width()/2) else None, add="+")
        canvas.bind('<Configure>', lambda event: (secondFrame.winfo_width()) != (event.width) if canvas.moveto(window, canvas.winfo_width()/4, 0) else None, add="+")

        # self.loadGames(master, 'a', secondFrame)
        
        data = self.getFileNames()

        self.comboboxDate = ttk.Combobox(secondFrame)
        self.comboboxDate.configure(
            font='terminal 8',
            cursor="cross",
            justify="left",
            state="readonly",
            values=[]
        )
        self.comboboxDate.grid(column="2", row="0", sticky="ne", pady=10, padx=10)
        self.ghostNum = self.comboboxDate.get()

        self.comboboxGN = ttk.Combobox(secondFrame)
        self.comboboxGN.configure(
            font='terminal 8',
            cursor="cross",
            justify="left",
            state="readonly",
            values= []
        )
        self.comboboxGN.grid(column="1", row="0", sticky="ne", pady=10, padx=10)
        self.comboboxGN.bind("<<ComboboxSelected>>", lambda event: self.updateDate(data))

        self.comboboxUN = ttk.Combobox(secondFrame)
        self.comboboxUN.configure(
            font='terminal 8',
            cursor="cross",
            justify="left",
            state="readonly",
            values=list(set([name[0] for name in data] + [""]))
        )
        self.comboboxUN['values']
        self.comboboxUN.grid(column="0", row="0", sticky="ne", pady=10, padx=10)
        self.comboboxUN.bind("<<ComboboxSelected>>", lambda event: self.updateGameName(data))
        
        self.loadGames(master, secondFrame)
        
        #Ui
        self.ui_image=tk.PhotoImage(file=master.getPath("LGui.png"))
        self.uiimg = secondFrame.create_image(master.winfo_width()/2, master.winfo_height()/2, image=self.ui_image, anchor = tk.CENTER)
        secondFrame.bind('<Configure>', lambda event: self.slowerScroll(canvas, secondFrame, self.uiimg), add="+")
        
        #Background
        self.background_image=tk.PhotoImage(file=master.getPath("HSBackground.png"))
        self.bgimg = canvas.create_image(0, 0, image=self.background_image, anchor = "nw", tag="background")
        secondFrame.bind('<Configure>', lambda event: self.onScroll(canvas, canvas, self.bgimg, event), add="+")

        #Find button
        self.f_path = "find.png"
        self.F_image = tk.PhotoImage(file = master.getPath(self.f_path))
        self.fimg = canvas.create_image(master.winfo_width()*0.75,master.winfo_height()*0.01, image= self.F_image, anchor = tk.CENTER)
        canvas.tag_bind(self.fimg, "<Button-1>", lambda event: self.loadGames(master, secondFrame), add="+")
        secondFrame.bind('<Configure>', lambda event: self.onScroll(canvas, canvas, self.fimg, event, master.winfo_width()*0.75, master.winfo_height()*0.01), add="+")

        #Create button
        self.c_path = "imgC.png"
        self.C_image = tk.PhotoImage(file = master.getPath(self.c_path))
        self.cimg = canvas.create_image(master.winfo_width()*0.8,master.winfo_height()*0.5, image= self.C_image, anchor = tk.CENTER)
 
        self.CP_image = tk.PhotoImage(file = master.getPath("imgCP.png"))
        canvas.tag_bind(self.cimg, "<Enter>", lambda event: setattr(self, 'c_path', "imgCP.png"), add="+")
        canvas.tag_bind(self.cimg, "<Enter>", lambda event: master.resizer(master.getPath(self.c_path), canvas, self.cimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        canvas.tag_bind(self.cimg, "<Leave>", lambda event: setattr(self, 'c_path', "imgC.png"), add="+")
        canvas.tag_bind(self.cimg, "<Leave>", lambda event: master.resizer(master.getPath(self.c_path), canvas, self.cimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        canvas.tag_bind(self.cimg, "<Button-1>", lambda event: self.loadGame(master), add="+")
        secondFrame.bind('<Configure>', lambda event: self.onScroll(canvas, canvas, self.cimg, event, master.winfo_width()*0.8, master.winfo_height()*0.5), add="+")

        #Back button
        self.b_path = "imgB.png"
        self.B_image = tk.PhotoImage(file = master.getPath(self.b_path))
        self.bimg = canvas.create_image(master.winfo_width()*0.07,master.winfo_height()*0.5, image= self.B_image, anchor = tk.CENTER)
 
        self.BP_image = tk.PhotoImage(file = master.getPath("imgBP.png"))
        canvas.tag_bind(self.bimg, "<Enter>", lambda event: setattr(self, 'b_path', "imgBP.png"), add="+")
        canvas.tag_bind(self.bimg, "<Enter>", lambda event: master.resizer(master.getPath(self.b_path), canvas, self.bimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        canvas.tag_bind(self.bimg, "<Leave>", lambda event: setattr(self, 'b_path', "imgB.png"), add="+")
        canvas.tag_bind(self.bimg, "<Leave>", lambda event: master.resizer(master.getPath(self.b_path), canvas, self.bimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        canvas.tag_bind(self.bimg, "<Button-1>", lambda event: self.deleteCanvas(master, canvas, "HomeScreen"), add="+")
        secondFrame.bind('<Configure>', lambda event: self.onScroll(canvas, canvas, self.bimg, event, master.winfo_width()*0.07, master.winfo_height()*0.5), add="+")
       
        #Images resizing
        canvas.bind('<Configure>', lambda event: resizeWin(event),add="+")
        def resizeWin(event, *args):
            flag = args[0] if len(args)!=0 else False
            if(flag or ((master.width, master.height) != (event.width, event.height))):
                master.resizer(master.getPath("HSBackground.png"), canvas, self.bgimg, master.winfo_width(), master.winfo_height())
                master.resizer(master.getPath(self.c_path), canvas, self.cimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08))
                master.resizer(master.getPath(self.b_path), canvas, self.bimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08))
                master.resizer(master.getPath(self.f_path), canvas, self.fimg, int(master.winfo_width()*0.09), int(master.winfo_height()*0.1))
                master.resizer(master.getPath("LGui.png"), secondFrame, self.uiimg, int(master.winfo_width()*1.2), int(master.winfo_height()))
                self.slowerScroll(canvas, secondFrame, self.uiimg)
                self.onScroll(canvas, canvas, self.bimg, None, master.winfo_width()*0.07, master.winfo_height()*0.5)
                self.onScroll(canvas, canvas, self.cimg, None, master.winfo_width()*0.8, master.winfo_height()*0.5)
                self.onScroll(canvas, canvas, self.fimg, None, master.winfo_width()*0.75, master.winfo_height()*0.01)
                pass
                
        resizeWin(None, True)
        self.canvas = canvas
        self.alterMenu(master, secondFrame)
        

    def onScroll(self, canvas1, canvas2, item, event, *args):
        t = Thread(target = self.scrolled(canvas1, canvas2, item, event, *args))
        t.start()

    def scrolled(self, canvas1, canvas2, item, event, *args):
        x, y = canvas1.canvasx(0), canvas1.canvasy(0)
        if(args):
            a, b = canvas1.canvasx(args[0]), canvas1.canvasy(args[1])
            canvas2.moveto(item, a, b)
        else:
            canvas2.moveto(item, x, y)

    def slowerScroll(self, canvas1, canvas2, item):
        t = Thread(target = self.slower(canvas1, canvas2, item))
        t.start()

    def slower(self, canvas1, canvas2, item):
        x, y = canvas1.canvasx(0), canvas1.canvasy(0)
        canvas2.moveto(item, x, y)

    def getFileNames(self):
        directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        data = []
        for file in os.listdir(directory):
            if file.endswith(".ini"):
                uName, gName, date = file.split('#')
                date = date[:len(date)-4]
                data.append((uName, gName, date))
        return data

    def updateGameName(self, data):
        self.comboboxGN['values'] = [name[1] for name in data if name[0] == self.comboboxUN.get()] + [""]
        self.comboboxGN.set('')
        self.comboboxDate.set('')

    def updateDate(self, data):
        self.comboboxDate['values'] = list(set([name[2] for name in data if name[0] == self.comboboxUN.get() and name[1] == self.comboboxGN.get()] + [""]))
        self.comboboxDate.set('')

    def loadGames(self, master, frame):
        for one in frame.winfo_children():
            if one.winfo_class() == 'Button':
                print('lala')
                one.destroy()
        
        self.buttons = []
        directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        fileName = []
        # if self.comboboxUN.get() != "":
        #     fileName += self.comboboxUN.get()+'#'

        # if self.comboboxGN.get() != "":
        #     fileName += self.comboboxGN.get()+'#'

        # if self.comboboxDate.get() != "":
        #     fileName += self.comboboxDate.get()
        
        # if fileName == "":
        #     fileName += '.ini'

        if self.comboboxUN.get() != "":
            fileName.append(self.comboboxUN.get())

        if self.comboboxGN.get() != "":
            fileName.append(self.comboboxGN.get())

        if self.comboboxDate.get() != "":
            fileName.append(self.comboboxDate.get())
        
        fileName.append('.ini')
        ind = -1

        for file in os.listdir(directory):
            flag = True
            for value in fileName:
                if value not in file:
                    flag = False
            if flag:
                ind+=1
                parser = ConfigParser()
                parser.read(master.getPath(file))
                data = {}
                for section in parser.sections():
                    for key, value in parser.items(section):
                        if value.isdigit():
                            data[key] = int(value)
                        elif value.isalnum() or ('-' in value):
                            data[key] = value
                        else:
                            data[key] = eval(value)
                     
                   
                    info=' User name: {0:>15} Game name: {1:>16}\n Date: {2:>20} Side: {3:>21}\n Ghost fac: {4:>15} Finish fac: {5:>15}\n Treasures: {6:>15} Ghosts: {7:>19}'.format(data['username'], data['gamename'], data['date'],data['sidelen'], data['ghostfactor'], data['finishfactor'],data['treasurenum'], data['ghostnum'])

            
                    self.buttons.append(file)
                    it = tk.Button(frame, text=info, height=10, bg='#d0c4b4', relief=tk.RAISED, font=("terminal 10"), justify='left', anchor='center', padx=5)
                    it.grid(row = ind+1, column=0, columnspan = 3, pady=2, padx=2, sticky='nswe')
                    it.bind("<Button-1>", lambda event: self.clicked(event, frame))

    def clicked(self, event, frame):
        event.widget.config(relief=tk.SUNKEN, bg='#c0b4ac', command="")
        self.toLoad = self.buttons[event.widget.grid_info()['row']-1]
        print(event.widget.grid_info()['row']-1)
        print('lala')
        for one in frame.winfo_children():
            if one.winfo_class() == 'Button':
                if(one!=event.widget):
                    one.config(relief=tk.RAISED, bg='#d0c4b4')
        return 'break'
        
    def deleteCanvas(self, master, canvas, name, *args, **kwargs):
        # self.unbind('<Configure>')
        # self.ffs.unbind_all("<Enter>")
        # self.ffs.unbind_all("<Leave>")
        # self.ffs.unbind_all("<Button-1>")
        # self.ffs.delete('all')
        # self.canvas.unbind_all("<Enter>")
        # self.canvas.unbind_all("<Leave>")
        # self.canvas.unbind_all("<Button-1>")
        # self.canvas.delete('all')
        # print(args)
        master.show_frame(name, *args, **kwargs)

    def showWarning(self, kill):
        if(kill):
            if 'message_window' in locals():
                message_window.destroy()
        else:
            message_window = tk.Toplevel()
            message_window.title("Invalid Data")
            label = tk.Label(message_window, text="Provided data is invalid!", font=("terminal 15"), justify=tk.LEFT)
            label.pack(padx=20, pady=15)
            ok = tk.Button(message_window, text="Ok", font=("terminal 12"), width=8, relief=tk.GROOVE,bd=3, command=lambda: message_window.destroy())
            ok.pack(padx=5, pady=10, side=tk.RIGHT)

    def loadGame(self, master):
        print(self.toLoad)
        if(len(self.toLoad)!=0):
            parser = ConfigParser()
            parser.read(master.getPath(self.toLoad))
            data = {}
            for section in parser.sections():
                for key, value in parser.items(section):
                    if value.isdigit():
                        data[key] = int(value)
                    elif (value.isalnum() or (('-' in value) and (('[') not in value))):
                        data[key] = value
                    else:
                        data[key] = eval(value)

            self.deleteCanvas(master, None, "DifferentMaze", data.pop('sidelen'), data.pop('finishfactor'),
                            data.pop('ghostfactor'), data.pop('ghostnum'), data.pop('treasurenum'), data.pop('gamename'), 
                            data.pop('username'), **data)
        else:
            self.showWarning(False)

    def alterMenu(self, master, secondFrame):
        master.deleteMenuBar('Menu')
        menubar = tk.Menu(master, borderwidth=0)
        fileMenu = tk.Menu(menubar, background = "#d0c4b4",fg='#2a2e2c', tearoff=False, activebackground='#c0b4ac',activeforeground='#1c1c1c', borderwidth=0, font='terminal 12', relief=tk.RAISED)
        for label, command, shortcut_text, shortcut in (
                ("Create...", lambda: self.loadGame(master), "Ctrl+C", "<Control-c>"),
                ("Back...", lambda: self.deleteCanvas(master, self.canvas, "HomeScreen"), "Ctrl+B", "<Control-b>"),
                ("Find...", lambda: self.loadGames(master, secondFrame), "Ctrl+F", "<Control-f>"),
                (None, None, None, None),
                ("Quit", lambda: master.quit(), "Ctrl+Q", "<Control-q>")
                ):
            if label is None:
                fileMenu.add_separator()
            else:
                fileMenu.add_command(label=label,command=command, accelerator=shortcut_text)
                master.bind(shortcut, command)
        menubar.add_cascade(label="Menu", menu=fileMenu)

        master.addMenuBar(fileMenu)
   