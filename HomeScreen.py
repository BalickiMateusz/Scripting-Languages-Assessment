import tkinter as tk

class HomeScreen(tk.Frame):
    def __init__(self, master, container):
        super().__init__(container)
        master.update_idletasks()
        canvas = tk.Canvas(self, height = master.winfo_width(), width = master.winfo_height())
        canvas.pack(side = "top", fill = "both", expand = True)
        #Background
        self.background_image=tk.PhotoImage(file=master.getPath("HSBackground.png"))
        self.bgimg = canvas.create_image(0, 0, image=self.background_image, anchor = "nw", tag="background")
        master.toolbar(canvas)

        #New Game button
        self.ng_path = "imgNG.png"
        self.NG_image = tk.PhotoImage(file = master.getPath(self.ng_path))
        self.ngimg = canvas.create_image(master.winfo_width()/2,master.winfo_height()*0.41, image= self.NG_image, anchor = tk.CENTER, tag="button")
 
        self.NGP_image = tk.PhotoImage(file = master.getPath("imgNGP.png"))
        canvas.tag_bind(self.ngimg, "<Enter>", lambda event: setattr(self, 'ng_path', "imgNGP.png"), add="+")
        canvas.tag_bind(self.ngimg, "<Enter>", lambda event: master.resizer(master.getPath(self.ng_path), canvas, self.ngimg, int(master.winfo_width()*0.28), int(master.winfo_height()*0.09)), add="+")
        canvas.tag_bind(self.ngimg, "<Leave>", lambda event: setattr(self, 'ng_path', "imgNG.png"), add="+")
        canvas.tag_bind(self.ngimg, "<Leave>", lambda event: master.resizer(master.getPath(self.ng_path), canvas, self.ngimg, int(master.winfo_width()*0.28), int(master.winfo_height()*0.09)), add="+")
        canvas.tag_bind(self.ngimg, "<Button-1>", lambda event: self.deleteCanvas(master, canvas, 'NewGame'), add="+")

        #Load Game button
        self.lg_path = "imgLG.png"
        self.LG_image = tk.PhotoImage(file = master.getPath(self.lg_path))
        self.lgimg = canvas.create_image(master.winfo_width()/2,master.winfo_height()/2, image= self.LG_image, anchor = tk.CENTER, tag="button")
 
        self.LGP_image = tk.PhotoImage(file = master.getPath("imgLGP.png"))
        canvas.tag_bind(self.lgimg, "<Enter>", lambda event: setattr(self, 'lg_path', "imgLGP.png"), add="+")
        canvas.tag_bind(self.lgimg, "<Enter>", lambda event: master.resizer(master.getPath(self.lg_path), canvas, self.lgimg, int(master.winfo_width()*0.28), int(master.winfo_height()*0.09)), add="+")
        canvas.tag_bind(self.lgimg, "<Leave>", lambda event: setattr(self, 'lg_path', "imgLG.png"), add="+")
        canvas.tag_bind(self.lgimg, "<Leave>", lambda event: master.resizer(master.getPath(self.lg_path), canvas, self.lgimg, int(master.winfo_width()*0.28), int(master.winfo_height()*0.09)), add="+")
        canvas.tag_bind(self.lgimg, "<Button-1>", lambda event: self.deleteCanvas(master, canvas, 'LoadGame'), add="+")

        #Options button
        self.opt_path = "imgOPT.png"
        self.OPT_image = tk.PhotoImage(file = master.getPath(self.opt_path))
        self.optimg = canvas.create_image(master.winfo_width()*0.43,master.winfo_height()*0.69, image= self.OPT_image, anchor = tk.CENTER, tag="button")
 
        self.OPTP_image = tk.PhotoImage(file = master.getPath("imgOPTP.png"))
        canvas.tag_bind(self.optimg, "<Enter>", lambda event: setattr(self, 'opt_path', "imgOPTP.png"), add="+")
        canvas.tag_bind(self.optimg, "<Enter>", lambda event: master.resizer(master.getPath(self.opt_path), canvas, self.optimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.09)), add="+")
        canvas.tag_bind(self.optimg, "<Leave>", lambda event: setattr(self, 'opt_path', "imgOPT.png"), add="+")
        canvas.tag_bind(self.optimg, "<Leave>", lambda event: master.resizer(master.getPath(self.opt_path), canvas, self.optimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.09)), add="+")
        canvas.tag_bind(self.optimg, "<Button-1>", lambda event: master.showOptions(), add="+")
        
        #Quit Game button
        self.qg_path = "imgQG.png"
        self.QG_image = tk.PhotoImage(file = master.getPath(self.qg_path))
        self.qgimg = canvas.create_image(master.winfo_width()*0.57,master.winfo_height()*0.69, image= self.QG_image, anchor = tk.CENTER, tag="button")
 
        self.QGP_image = tk.PhotoImage(file = master.getPath("imgQGP.png"))
        canvas.tag_bind(self.qgimg, "<Enter>", lambda event: setattr(self, 'qg_path', "imgQGP.png"), add="+")
        canvas.tag_bind(self.qgimg, "<Enter>", lambda event: master.resizer(master.getPath(self.qg_path), canvas, self.qgimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.09)), add="+")
        canvas.tag_bind(self.qgimg, "<Leave>", lambda event: setattr(self, 'qg_path', "imgQG.png"), add="+")
        canvas.tag_bind(self.qgimg, "<Leave>", lambda event: master.resizer(master.getPath(self.qg_path), canvas, self.qgimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.09)), add="+")
        canvas.tag_bind(self.qgimg, "<Button-1>", lambda event: master.quit(), add="+")

        #Imges resizing
        self.bind('<Configure>', lambda event: resizeWin(event))
        def resizeWin(event, *args):
            flag = args[0] if len(args)!=0 else False
            if(flag or ((master.width, master.height) != (event.width, event.height))):
                master.resizer(master.getPath("HSBackground.png"), canvas, self.bgimg, master.winfo_width(), master.winfo_height())
                master.resizer(master.getPath(self.ng_path), canvas, self.ngimg, int(master.winfo_width()*0.28), int(master.winfo_height()*0.09))
                master.resizer(master.getPath(self.lg_path), canvas, self.lgimg, int(master.winfo_width()*0.28), int(master.winfo_height()*0.09))
                master.resizer(master.getPath(self.opt_path), canvas, self.optimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.09))
                master.resizer(master.getPath(self.qg_path), canvas, self.qgimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.09))
        resizeWin(None, True)
        self.canvas = canvas

    def deleteCanvas(self, master, canvas, name):
        self.unbind('<Configure>')
        canvas.unbind_all("<Enter>")
        canvas.unbind_all("<Leave>")
        canvas.unbind_all("<Button-1>")
        canvas.delete('all')
        master.show_frame(name)

    def createMenubar(self, master):
        menubar = tk.Menu(master, borderwidth=0)
        helpMenu = tk.Menu(menubar, background = "#d0c4b4",fg='#2a2e2c', tearoff=False, activebackground='#c0b4ac',activeforeground='#1c1c1c', borderwidth=0, font='terminal 12', relief=tk.RAISED)
        
        howto = """ 
                    To play this game, please click "load game" to load Your saved game, or press "New Game" to\n
                    create new game with a great passion for IT. Amateur software developer. Willing to learn\n
                    and gain knowledge."""

        loadGame = """ 
                    To load new game, please click 'Load Game' button i main menu. You can choose games\n
                    based on certain player, then within names of his games and dates of creation."""
        
        creatGame = """ 
                    To create new game, please click 'New Game' button i main menu. You can choose game's\n
                    settings like game name, user name (they both need to be alphanumerical, max 20 chars.\n
                    You can choose number of rows and columns of maze, how many treasures will be to collect\n
                    before finish, number of ghosts that will hunt you. Min. distances are minimum distances\n
                    at which specific game elements will have a chance to spawn, related to Your starting\n
                    point."""

        treasures = """ 
                    Treasures are very precious! Thus, you want to collect them all before escaping the maze!\n
                    Standing on finish point without collecting every treasure won't have any effect!"""

        ghosts = """ 
                    Those are monsters that are hunting You! If monster reaches You, he eats you and you die.\n
                    You can try to escape ghost by bravely jumping into him!"""

        shortest = """ 
                    After each game, despite it's result, we will show you the most optimal path you should\n
                    had follow!"""

        for label, command in (
                ("How to play?", lambda: self.showWarning("How to play", howto)),
                ("Loading games...", lambda: self.showWarning("Loading games", loadGame)),
                ("Creating new games...", lambda: self.showWarning("Creating new games", creatGame)),
                (None, None),
                ("The game itself!", lambda: print("")),
                ):
            if label is None:
                helpMenu.add_separator()
            else:
                if label == "The game itself!":
                    subMenu = tk.Menu(helpMenu, background = "#d0c4b4",fg='#2a2e2c', tearoff=False, activebackground='#c0b4ac',activeforeground='#1c1c1c', borderwidth=0, font='terminal 12', relief=tk.RAISED)
                    subMenu.add_command(label='Treasures',command=lambda: self.showWarning("Treasures", treasures))
                    subMenu.add_command(label='Ghosts',command=lambda: self.showWarning("Ghosts", ghosts))
                    subMenu.add_command(label='Shortest Path',command=lambda: self.showWarning("Shortest Path", shortest))
                    helpMenu.add_cascade(label=label, menu=subMenu)
                else:
                    helpMenu.add_command(label=label,command=command)
        menubar.add_cascade(label="Help", menu=helpMenu)
        
        author = """ 
                    Hi, my name is Balicki Mateusz. An ambitious, hard-working Applied Computer Science undergraduate\n 
                    with a great passion for IT. Amateur software developer. Willing to learn and gain knowledge."""
        game = """ 
                    This game is all about running away from monsters. To win, you have to pick all treasures and go\n
                    to the finish point!"""
        dedication = """ 
                    To my friends, teacher, whole family and people around me. You are great!\n"""
 
        aboutMenu = tk.Menu(menubar, background = "#d0c4b4",fg='#2a2e2c', tearoff=False, activebackground='#c0b4ac',activeforeground='#1c1c1c', borderwidth=0, font='terminal 12', relief=tk.RAISED)
        for label, command in (
                ("Author...", lambda: self.showWarning("Author", author)),
                ("Game...", lambda: self.showWarning("Game", game)),
                (None, None),
                ("Dedication...", lambda: self.showWarning("Dedication", dedication)),
                ):
            if label is None:
                aboutMenu.add_separator()
            else:
                aboutMenu.add_command(label=label,command=command)
        menubar.add_cascade(label="About", menu=aboutMenu)

        fullScreen = tk.BooleanVar()

        optionsMenu = tk.Menu(menubar, background = "#d0c4b4",fg='#2a2e2c', tearoff=False, activebackground='#c0b4ac',activeforeground='#1c1c1c', borderwidth=0, font='terminal 12', relief=tk.RAISED)
        for label, command, shortcut_text, shortcut in (
                ("Options", lambda: master.showOptions(), "Ctrl+O", "<Control-o>"),
                (None, None, None, None)
                ):
            if label is None:
                optionsMenu.add_separator()
            else:
                optionsMenu.add_command(label=label,command=command, accelerator=shortcut_text)
                master.bind(shortcut, command)
        optionsMenu.add_checkbutton(label="Full Screen Checkbox", onvalue=True, offvalue=False, variable=fullScreen, command = lambda: master.fullScreen(fullScreen.get()))
        menubar.add_cascade(label="Options", menu=optionsMenu)

        fileMenu = tk.Menu(menubar, background = "#d0c4b4",fg='#2a2e2c', tearoff=False, activebackground='#c0b4ac',activeforeground='#1c1c1c', borderwidth=0, font='terminal 12', relief=tk.RAISED)
        for label, command, shortcut_text, shortcut in (
                ("New...", lambda: self.deleteCanvas(master, self.canvas, 'NewGame'), "Ctrl+N", "<Control-n>"),
                ("Load...", lambda: self.deleteCanvas(master, self.canvas, 'LoadGame'), "Ctrl+L", "<Control-l>"),
                ("Options", lambda: print('aaaa'), "Ctrl+O", "<Control-o>"),
                (None, None, None, None),
                ("Quit", lambda: master.quit(), "Ctrl+Q", "<Control-q>")
                ):
            if label is None:
                fileMenu.add_separator()
            else:
                fileMenu.add_command(label=label,command=command, accelerator=shortcut_text)
                master.bind(shortcut, command)
        menubar.add_cascade(label="Menu", menu=fileMenu)
        return menubar

    def showWarning(self, title, text):
        message_window = tk.Toplevel()
        message_window.title(title)
        label = tk.Label(message_window, text=text, font=("terminal 15"), justify=tk.LEFT)
        label.pack(padx=20, pady=15)
        ok = tk.Button(message_window, text="Ok", font=("terminal 12"), width=8, relief=tk.GROOVE,bd=3, command=lambda: message_window.destroy())
        ok.pack(padx=5, pady=10, side=tk.RIGHT)