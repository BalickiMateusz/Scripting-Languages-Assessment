import tkinter as tk
from tkinter import StringVar, ttk

class NewGame(tk.Frame):
    def __init__(self, master, container):
        super().__init__(container)

        master.update_idletasks()
        canvas = tk.Canvas(self, height = master.winfo_width(), width = master.winfo_height())
        canvas.pack(side = "top", fill = "both", expand = True)
        self.alterMenu(master)

        #Canvas grid configure
        canvas.grid_rowconfigure(0, weight = 4)
        canvas.grid_rowconfigure(1, weight = 1)
        canvas.grid_rowconfigure(2, weight = 1)
        canvas.grid_rowconfigure(3, weight = 1)
        canvas.grid_rowconfigure(4, weight = 1)
        canvas.grid_rowconfigure(5, weight = 4)

        canvas.grid_columnconfigure(0, weight = 3)
        canvas.grid_columnconfigure(1, weight = 2)
        canvas.grid_columnconfigure(2, weight = 1)
        canvas.grid_columnconfigure(3, weight = 1)
        canvas.grid_columnconfigure(4, weight = 2)
        canvas.grid_columnconfigure(5, weight = 3)
        
        #Background
        self.background_image=tk.PhotoImage(file=master.getPath("HSBackground.png"))
        self.bgimg = canvas.create_image(0, 0, image=self.background_image, anchor = "nw", tag="background")

        #Ui
        self.ui_image=tk.PhotoImage(file=master.getPath("NGui.png"))
        self.uiimg = canvas.create_image(master.winfo_width()/2, master.winfo_height()/2, image=self.ui_image, anchor = tk.CENTER, tag="button")

        self.dataInputs(canvas, master)

        #Create button
        self.c_path = "imgC.png"
        self.C_image = tk.PhotoImage(file = master.getPath(self.c_path))
        self.cimg = canvas.create_image(master.winfo_width()*0.72,master.winfo_height()*0.75, image= self.C_image, anchor = tk.CENTER, tag="button")
 
        self.CP_image = tk.PhotoImage(file = master.getPath("imgCP.png"))
        canvas.tag_bind(self.cimg, "<Enter>", lambda event: setattr(self, 'c_path', "imgCP.png"), add="+")
        canvas.tag_bind(self.cimg, "<Enter>", lambda event: master.resizer(master.getPath(self.c_path), canvas, self.cimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        canvas.tag_bind(self.cimg, "<Leave>", lambda event: setattr(self, 'c_path', "imgC.png"), add="+")
        canvas.tag_bind(self.cimg, "<Leave>", lambda event: master.resizer(master.getPath(self.c_path), canvas, self.cimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        canvas.tag_bind(self.cimg, "<Button-1>", lambda event: self.deleteCanvas(master, canvas, "DifferentMaze"), add="+")

        #Back button
        self.b_path = "imgB.png"
        self.B_image = tk.PhotoImage(file = master.getPath(self.b_path))
        self.bimg = canvas.create_image(master.winfo_width()*0.28,master.winfo_height()*0.75, image= self.B_image, anchor = tk.CENTER, tag="button")
 
        self.BP_image = tk.PhotoImage(file = master.getPath("imgBP.png"))
        canvas.tag_bind(self.bimg, "<Enter>", lambda event: setattr(self, 'b_path', "imgBP.png"), add="+")
        canvas.tag_bind(self.bimg, "<Enter>", lambda event: master.resizer(master.getPath(self.b_path), canvas, self.bimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        canvas.tag_bind(self.bimg, "<Leave>", lambda event: setattr(self, 'b_path', "imgB.png"), add="+")
        canvas.tag_bind(self.bimg, "<Leave>", lambda event: master.resizer(master.getPath(self.b_path), canvas, self.bimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        canvas.tag_bind(self.bimg, "<Button-1>", lambda event: self.deleteCanvas(master, canvas, "HomeScreen"), add="+")

        #Images resizing
        self.bind('<Configure>', lambda event: resizeWin(event))
        def resizeWin(event, *args):
            flag = args[0] if len(args)!=0 else False
            if(flag or ((master.width, master.height) != (event.width, event.height))):
                master.resizer(master.getPath("HSBackground.png"), canvas, self.bgimg, master.winfo_width(), master.winfo_height())
                master.resizer(master.getPath("NGui.png"), canvas, self.uiimg, int(master.winfo_width()*0.76), int(master.winfo_height()*0.95))
                master.resizer(master.getPath(self.c_path), canvas, self.cimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08))
                master.resizer(master.getPath(self.b_path), canvas, self.bimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08))
        resizeWin(None, True)
        self.canvas = canvas
        master.toolbar(canvas)

    def dataInputs(self, canvas, master):
        #New game name
        self.labelNG = canvas.create_text(master.winfo_width()*0.35, master.winfo_height()*0.22, text="New game name:", anchor="e", tag="text", font='terminal 12')

        svNG = StringVar(value='New game...')
        self.entryNG = tk.Entry(canvas, fg="grey", font='terminal 12')
        svNG.trace("w", lambda name, index, mode, sv=svNG: self.get_string(self.entryNG))
        self.entryNG.configure(textvariable=svNG)
        self.entryNG.bind("<Button-1>", lambda event:self.first_click(self.entryNG))
        self.entryNG.grid(column="2", row="1", sticky="ne")
        self.ngName = self.entryNG.get()

        self.labelUN = canvas.create_text(master.winfo_width()*0.35, master.winfo_height()*0.37, text="User name:", anchor="e", tag="text", font='terminal 12')

        svUN = StringVar(value='User name...')
        self.entryUN = tk.Entry(canvas, fg="grey", font='terminal 12')
        svUN.trace("w", lambda name, index, mode, sv=svUN: self.get_string(self.entryUN))
        self.entryUN.configure(textvariable=svUN)
        self.entryUN.bind("<Button-1>", lambda event:self.first_click(self.entryUN))
        self.entryUN.grid(column="2", row="2", sticky="ne")
        self.uName = self.entryUN.get()

        self.labelRC = canvas.create_text(master.winfo_width()*0.35, master.winfo_height()*0.51, text="Rows and columns:", anchor="e", tag="text", font='terminal 12')

        self.scaleRC = tk.Scale(canvas)
        self.rowsAndColumns = tk.IntVar(value=0)
        self.scaleRC.configure(
            cursor="cross", from_="10", length="190", orient="horizontal",
            state="normal", to="60", variable=self.rowsAndColumns, tickinterval=10, font='terminal 10'
        )
        self.scaleRC.grid(column="2", row="3", sticky="ne")

        self.labelTN = canvas.create_text(master.winfo_width()*0.35, master.winfo_height()*0.66, text="Treasures before finish:", anchor="e", tag="text", font='terminal 12')

        self.scaleTN = tk.Scale(canvas)
        self.treasuresNum = tk.IntVar(value=0)
        self.scaleTN.configure(
            cursor="cross", from_="0", length="190", orient="horizontal",
            state="normal", to="8", variable=self.treasuresNum, tickinterval=1, font='terminal 10'
        )
        self.scaleTN.grid(column="2", row="4", sticky="ne")

        self.labelFD = canvas.create_text(master.winfo_width()*0.67, master.winfo_height()*0.22, text="Finish min. distance:", anchor="e", tag="text", font='terminal 12')

        self.scaleFD = tk.Scale(canvas)
        self.finishDist = tk.IntVar(value=0)
        self.scaleFD.configure(
            cursor="cross", from_="0", length="190", orient="horizontal", resolution=0.05,
            state="normal", to="0.7", variable=self.finishDist, tickinterval=0.2, font='terminal 10'
        )
        self.scaleFD.grid(column="4", row="1", sticky="ne")

        self.labelGD = canvas.create_text(master.winfo_width()*0.67, master.winfo_height()*0.37, text="Ghost min. distance:", anchor="e", tag="text", font='terminal 12')

        self.scaleGD = tk.Scale(canvas)
        self.ghostDist = tk.IntVar(value=0)
        self.scaleGD.configure(
            cursor="cross", from_="0", length="190", orient="horizontal", resolution=0.05,
            state="normal", to="0.7", variable=self.ghostDist, tickinterval=0.2, font='terminal 10'
        )
        self.scaleGD.grid(column="4", row="2", sticky="ne")

        self.labelGN = canvas.create_text(master.winfo_width()*0.67, master.winfo_height()*0.51, text="Number of ghosts:", anchor="e", tag="text", font='terminal 12')
             
        self.comboboxGN = ttk.Combobox(canvas)
        self.comboboxGN.configure(
            font='terminal 8',
            cursor="cross",
            justify="left",
            state="readonly",
            values=("0 ←easy peasyʕ •ᴥ•ʔ","1 ←beginner(✿◠‿◠)","2 ←bad dream\_(ツ)_/","3 ←will of iron☉_☉",
                    "4 ←ultra violence( °□° )","5 ←nightmare!(⌐■_■)")
        )
        self.comboboxGN.set("0 ← easy peasy")
        self.comboboxGN.grid(column="4", row="3", sticky="ne")
        self.ghostNum = self.comboboxGN.get()

    def first_click(self, widget):
        widget.delete(0, tk.END)
        widget.unbind("<Button-1>")
        widget.configure(fg="black")

    def get_string(self, widget):
        self.update_idletasks()
        message = widget.get()
        if((message.isalnum() or message=="") and len(message) < 20):
            widget.configure(bg="white")
        else:
            widget.configure(bg="red")

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
    
    def alterMenu(self, master):
        master.deleteMenuBar('Menu')
        menubar = tk.Menu(master, borderwidth=0)
        fileMenu = tk.Menu(menubar, background = "#d0c4b4",fg='#2a2e2c', tearoff=False, activebackground='#c0b4ac',activeforeground='#1c1c1c', borderwidth=0, font='terminal 12', relief=tk.RAISED)
        for label, command, shortcut_text, shortcut in (
                ("Create...", lambda: self.deleteCanvas(master, self.canvas, "DifferentMaze"), "Ctrl+C", "<Control-c>"),
                ("Back...", lambda: self.deleteCanvas(master, self.canvas, "HomeScreen"), "Ctrl+B", "<Control-b>"),
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

    def deleteCanvas(self, master, canvas, name):
        args = ()
        if(self.entryUN.cget('bg') == 'white' and self.entryNG.cget('bg') == 'white'):
            flag = True
        else:
            flag = False

        if(name == 'DifferentMaze'):
            args = (self.rowsAndColumns.get(), self.finishDist.get(), self.ghostDist.get(), int(self.comboboxGN.get()[0]), self.treasuresNum.get(), self.entryNG.get(), self.entryUN.get())
            if('New game...' in args):
                self.entryNG.configure(bg="red")
                flag = False
            if('User name...' in args):
                self.entryUN.configure(bg="red")
                flag = False
            
            if(not flag):
                self.showWarning(False)
                
        if(name == 'HomeScreen'):
            flag = True

        if(flag):
            self.showWarning(True)
            self.unbind('<Configure>')
            canvas.unbind_all("<Enter>")
            canvas.unbind_all("<Leave>")
            canvas.unbind_all("<Button-1>")
            canvas.delete('all')
            master.show_frame(name, *args)

   