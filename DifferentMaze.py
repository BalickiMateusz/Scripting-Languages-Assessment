from datetime import date
from operator import truediv
import tkinter as tk
from random import randint, choice
from Ghost import Ghost
from threading import Thread
from Dijkstra import Dijkstra
from PIL import ImageTk, Image
from configparser import *

class DifferentMaze(tk.Frame):
    def __init__(self, master, container, sideLen, finishFactor, ghostFactor, ghostNum, treasureNum, gameName, userName, **kwargs):
        #Randomized Prim's algorithm
        super().__init__(container)
        self.bind("<Key>", lambda event: self.move(master, event))
        master.update_idletasks()
        self.squareSize = (master.winfo_height()/(sideLen+2)) #Size of single square
        self.sideLen = sideLen #Number of rows and columns
        self.ghosts = []
        if 'ghosts' in kwargs:
            self.loadedGhosts = kwargs.pop('ghosts')
        else:
            self.loadedGhosts = []

        self.treasure_color = 'blue'

        #Ghost factor
        self.ghostFac = ghostFactor # max 0,7
        self.pac_color = 'Yellow'
        self.finish_color = 'Red'
        self.finishFac = finishFactor # max 0,7
        distFinish = int(self.sideLen * self.finishFac)
        self.start_color = '#32CD32'
        self.ghostNum = ghostNum
        self.treasureNum = treasureNum

        self.end = False
        self.stopBlinking = False
        master.update_idletasks()
        self.canvas = tk.Canvas(self, height = master.winfo_width(), width = master.winfo_height())
        self.canvas.pack(side = "top", fill = "both", expand = True)
        self.pathColor = "white"
        self.gameName = gameName
        self.userName = userName
        
        #Inner canvas                      
        self.canvas_side = (self.sideLen*self.squareSize) + self.squareSize*2
        self.ffs = tk.Canvas(self.canvas, width = self.canvas_side, height = self.canvas_side, bd=-2)
        
        self.canvas.grid_rowconfigure(1, weight=1)
        self.canvas.grid_columnconfigure(1, weight=1)
        self.ffs.grid(row = 1, column = 1, ipadx=0, ipady=0)
        
##########################################################
        if(len(kwargs)==0):
            
            #StartingPoint
            self.startX = randint(0, self.sideLen-1)
            self.startY = randint(0, self.sideLen-1)
            
            
            #Finish point
            
  
            possibleFinishes = self.possibleCoords(distFinish)
            self.finishX, self.finishY  = choice(possibleFinishes)

            #Map
            self.map = [['N' for _ in range(self.sideLen)]for _ in range(self.sideLen)]
            self.map[self.startX][self.startY] = 'Y'
            self.map[self.finishX][self.finishY] = 'Y'

            frontiers = self.findFrontiers(self.startX, self.startY)

            s = []

            for f in frontiers:
                s.append(f)

            while s:
                x, y = choice(s)
                s.remove([x, y])
                ns = self.findNeighbours(x,y)
                if ns:
                    nx, ny = choice(ns)
                    self.__connect(x, y, nx, ny)
                frontiers = self.findFrontiers(x, y)
                for f in frontiers:
                    s.append(f)

            for _ in range(randint(int(0.06*self.sideLen), int(0.12*self.sideLen))-int(0.5*self.ghostNum)):
                flag = True
                while flag:
                    xRand = randint(0, self.sideLen-1)
                    yRand = randint(0, self.sideLen-1)
                    if(self.map[xRand][yRand]=="N"):
                        self.map[xRand][yRand] = "Y"
                        flag = False

            list = []

            if(self.startX%2!=0):
                list.extend([(0, y) for y in range(0, self.sideLen)])

            if((self.sideLen-1-self.startX)%2!=0):
                list.extend([(self.sideLen-1, y) for y in range(0, self.sideLen)])

            if(self.startY%2!=0):
                list.extend([(x, 0) for x in range(0, self.sideLen)])

            if((self.sideLen-1-self.startY)%2!=0):
                list.extend([(x, self.sideLen-1) for x in range(0, self.sideLen)])

            for _ in range(randint(int(0.45*self.sideLen), int(0.8*self.sideLen))):
                if(list):
                    xRand, yRand = choice(list)
                    list.remove((xRand, yRand))
                    if(self.map[xRand][0]=="N"):
                        self.map[xRand][yRand] = "Y"

            self.treasuresList = []
            for _ in range(self.treasureNum):
                flag = True
                while flag:
                    xRand = randint(0, self.sideLen-1)
                    yRand = randint(0, self.sideLen-1)
                    if(self.map[xRand][yRand]=="Y" and (xRand, yRand) != (self.startX, self.startY)):
                        self.treasuresList.append((xRand, yRand))
                        self.draw(xRand, yRand, 'blue')
                        flag = False

            self.visitedTreasures = self.treasuresList.copy()
            self.dijkstra = Dijkstra(self.startX, self.startY, self.finishX, self.finishY, self.treasuresList, self.sideLen, self.map)
            self.shortestPath = self.dijkstra.shortestPath()
#################################################################
        else:
            self.startX = kwargs.pop('startx')
            self.startY = kwargs.pop('starty')
            self.finishX = kwargs.pop('finishx')
            self.finishY = kwargs.pop('finishy')
            self.map = kwargs.pop('map')
            self.treasuresList = kwargs.pop('treasureslist')
            self.visitedTreasures = kwargs.pop('visitedtreasures')
            # for treasure in self.visitedTreasures:
            #     print(treasure[0], treasure[1])
            #     self.draw(treasure[0], treasure[1], 'blue')
            self.shortestPath = kwargs.pop('shortestpath')
        
        #Background
        self.background_image=tk.PhotoImage(file=master.getPath("MBackground.png"))
        self.bgimg = self.canvas.create_image(0, 0, image=self.background_image, anchor = "nw", tag="background")


        #Background2
        self.background_image2=ImageTk.PhotoImage(file=master.getPath("Stone.png"))
        self.bg2img = self.ffs.create_image(0, 0, image=self.background_image2, anchor = "nw")
        #self.ffs.bind('<Configure>', lambda event: resizeWin(event, True))

        #SaveGame Button
        self.sg_path = "save.png"
        self.SG_image = tk.PhotoImage(file = master.getPath(self.sg_path))
        self.sgimg = self.canvas.create_image(master.winfo_width()*0.1,master.winfo_height()*0.1, image= self.SG_image, anchor = tk.CENTER, tag="button")
        self.canvas.tag_bind(self.sgimg, "<Button-1>", lambda event: self.saveGame(master), add="+")
        
        self.bind('<Configure>', lambda event: resizeWin(event))

        def resizeWin(event, *args):
            flag = args[0] if len(args)!=0 else False
            if(flag or ((master.width, master.height) != (event.width, event.height))):
                master.resizer(master.getPath("MBackground.png"), self.canvas, self.bgimg, master.winfo_width(), master.winfo_height())
                master.resizer(master.getPath(self.sg_path), self.canvas, self.sgimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.2))
                self.ffs.update_idletasks()
                master.resizer(master.getPath("Stone.png"), self.ffs, self.bg2img, self.ffs.winfo_reqwidth(), self.ffs.winfo_reqheight())

        resizeWin(None, True)
        
        self.create()
        for item in self.visitedTreasures:
            type(item[0])
            self.draw(item[0], item[1], 'blue')
        self.draw(self.startX, self.startY, self.start_color)
        self.draw(self.finishX, self.finishY, self.finish_color)
        self.alterMenu(master)
        master.toolbar(self.canvas)

    def startGhost(self, master):
        self.createGhost(master, self.ghostNum)

    def possibleCoords(self, distance):
        possibleCoords = []
        for x in range(self.sideLen):
            for y in range(self.sideLen):
                if(((x-self.startX)**2) + ((y-self.startY)**2) >= distance**2):
                    possibleCoords.append((x, y))

        return possibleCoords

    def create(self):
        for row in range(self.sideLen):
            for col in range(self.sideLen):
                if self.map[row][col] == 'Y':
                    color = 'White'
                elif self.map[row][col] == 'N':
                    color = 'black'
                self.draw(row, col, color)
    
    def draw(self, row, col, color):
        x1 = (col+1)*self.squareSize
        y1 = (row+1)*self.squareSize
        x2 = x1+self.squareSize
        y2 = y1+self.squareSize
        self.ffs.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
  
    def findNeighbours(self, ccr, ccc):
        neighbours = [[ccr, ccc-2], #left
                    [ccr, ccc+2], #right
                    [ccr-2, ccc], #top
                    [ccr+2, ccc]] #bottom
        
        found = []

        for i in neighbours:                                                                  
            if i[0] >= 0 and i[0] < self.sideLen and i[1] >= 0 and i[1] < self.sideLen:
                if self.map[i[0]][i[1]] == 'Y':
                    found.append(i[0:2])

        return found
     
    def findFrontiers(self, ccr, ccc):
        farNeighbours = [[ccr, ccc-2], [ccr, ccc+2], [ccr-2, ccc], [ccr+2, ccc]]
        frontiers = []
        
        for i in farNeighbours:                                                              
            if i[0] >= 0 and i[0] < self.sideLen and i[1] >= 0 and i[1] < self.sideLen:
                if self.map[i[0]][i[1]] == 'N':
                    frontiers.append(i[0:2])        

        return frontiers

    def __connect(self, x1, y1, x2, y2):
            x = (x1 + x2) // 2
            y = (y1 + y2) // 2
            self.map[x1][y1] = 'Y'
            self.map[x][y] = 'Y'

    def move(self, master, event):
        self.draw(self.startX, self.startY, self.pathColor)
        self.pathColor = "white"
        if event.char == "a":
            if(self.startY-1>=0):
                if self.map[self.startX][self.startY - 1] == "Y":
                    self.startY -= 1
        elif event.char == "d":
            if(self.startY+1<self.sideLen):
                if self.map[self.startX][self.startY + 1] == "Y":
                    self.startY += 1
        elif event.char == "w":
            if(self.startX-1>=0):
                if self.map[self.startX - 1][self.startY] == "Y":
                    self.startX -= 1
        elif event.char == "s":
            if(self.startX+1<self.sideLen):
                if self.map[self.startX + 1][self.startY] == "Y":
                    self.startX += 1
        if((self.startX, self.startY) in self.visitedTreasures):
            self.visitedTreasures.remove((self.startX, self.startY))
            print(len(self.visitedTreasures))
        elif((self.startX, self.startY) == (self.finishX, self.finishY) and len(self.visitedTreasures) == 0):
            t = Thread(target = lambda: self.blink(self.startX, self.startY, self.start_color, 'white'))
            t.start()
            self.endEvent(master, True)
        if ((self.startX, self.startY) == (self.finishX, self.finishY)):
            self.pathColor = "red"
        self.draw(self.startX, self.startY, "#32CD32")

    def getNormalNeighbours(self, x, y):
        neighbours = [[x, y-1], #left
                    [x, y+1], #right
                    [x-1, y], #top
                    [x+1, y]] #bottom
        found = []
        for i in neighbours:                                                                  
            if i[0] >= 0 and i[0] < self.sideLen and i[1] >= 0 and i[1] < self.sideLen:
                if self.map[i[0]][i[1]] == 'Y':
                    found.append((i[0], i[1]))
        return found

    def createGhost(self, master, num):
        if(len(self.loadedGhosts) == 0):
            distGhost = int(self.sideLen * self.ghostFac)
            possibleGhost = self.possibleCoords(distGhost)
            for i in range(num):
                gX, gY = choice(possibleGhost)
                possibleGhost.remove((gX, gY))
                ghost = Ghost(gX, gY)
                self.ghosts.append(ghost)
                self.map[ghost.x][ghost.y] = 'Y'
                self.draw(ghost.x, ghost.y, self.pac_color)
                t = Thread(target = lambda: self.moveGhost(master, ghost))
                t.start()
        else:
            for ghost in self.loadedGhosts:
                back, x, y, visited = ghost
                newGhost = Ghost(x, y)
                newGhost.back = back
                newGhost.visited = visited
                self.ghosts.append(newGhost)
                self.draw(newGhost.x, newGhost.y, self.pac_color)
                t = Thread(target = lambda: self.moveGhost(master, newGhost))
                t.start()

    def moveGhost(self, master, ghost):
        found = self.getNormalNeighbours(ghost.x, ghost.y)
        possibleMoves = list(set(found).difference(set(ghost.visited)))
        if len(possibleMoves)>0:
            if(ghost.back!=-2):
                ghost.back = -2
                temp = ghost.visited
                del temp[0:((len(ghost.visited)-(abs(ghost.back)-2))-1)]
                ghost.visited = temp
            dist = float('inf')
            for (x, y) in possibleMoves:
                temp = abs(x-self.startX) + abs(y-self.startY)
                if(dist > temp):
                    dist = temp
                    toVisit = (x, y)
            ghost.visited.append(toVisit)
  
        elif len(possibleMoves)==0:
            toVisit = ghost.visited[ghost.back]
            ghost.back = ghost.back - 1

        if(toVisit == (self.startX, self.startY)):
            t = Thread(target = lambda: self.blink(ghost.x, ghost.y, ghost.color, 'yellow'))
            t.start()
            del(ghost)
            self.endEvent(master, False)
        if(not self.end):
            self.draw(ghost.x, ghost.y, ghost.color)
            ghost.color = "white"
            ghost.x, ghost.y = toVisit

            if((ghost.x, ghost.y) in self.visitedTreasures):
                ghost.color = self.treasure_color

            if((ghost.x, ghost.y) == (self.finishX, self.finishY)):
                ghost.color = self.finish_color

            self.draw(ghost.x, ghost.y, "yellow")
            self.after(300, lambda: self.moveGhost(master, ghost))

    def blink(self, x, y, color1, color2):
        if(not self.stopBlinking):
            self.draw(x, y, color1)
            self.after(300, lambda: self.blink(x, y, color2, color1))

    def endEvent(self, master, result):
        self.end = True
        self.canvas.unbind_all("<Enter>")
        self.canvas.unbind_all("<Leave>")
        self.canvas.unbind_all("<Button-1>")
        self.unbind_all("<Key>")
        self.unbind('<Key>')

        for x, y in self.shortestPath:
            if((x, y) not in (self.treasuresList+[(self.startX, self.startY), (self.finishX, self.finishY)])):
                self.draw(x, y, 'purple')

        #Lost image
        self.end_image=ImageTk.PhotoImage(file=master.getPath("transparency.png"))
        self.eimg = self.canvas.create_image(0, 0, image=self.end_image, anchor = "nw", tag="button")
        self.ffs.tag_raise(self.eimg)

        if(result):
            end_file = master.getPath("win.png")
        else:
            end_file = master.getPath("lost.png")

        self.end_text=ImageTk.PhotoImage(file=end_file)
        self.eimg2 = self.ffs.create_image(0, 0, image=self.end_text, anchor = "nw", tag="button")
        self.ffs.tag_raise(self.eimg2)
        self.bind('<Configure>', lambda event: resizeEnd(event), add="+")

        #PlayAgain button
        self.pa_path = "imgPA.png"
        self.PA_image = tk.PhotoImage(file = master.getPath(self.pa_path))
        self.paimg = self.ffs.create_image(self.ffs.winfo_width()*0.68,self.ffs.winfo_height()*0.75, image= self.PA_image, anchor = tk.CENTER, tag="button")

        self.CP_image = tk.PhotoImage(file = master.getPath("imgPAP.png"))
        self.ffs.tag_bind(self.paimg, "<Enter>", lambda event: setattr(self, 'pa_path', "imgPAP.png"), add="+")
        self.ffs.tag_bind(self.paimg, "<Enter>", lambda event: master.resizer(master.getPath(self.pa_path), self.ffs, self.paimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        self.ffs.tag_bind(self.paimg, "<Leave>", lambda event: setattr(self, 'pa_path', "imgPA.png"), add="+")
        self.ffs.tag_bind(self.paimg, "<Leave>", lambda event: master.resizer(master.getPath(self.pa_path), self.ffs, self.paimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        self.ffs.tag_bind(self.paimg, "<Button-1>", lambda event: self.deleteCanvas(master, "DifferentMaze", self.sideLen, self.finishFac, self.ghostFac, self.ghostNum, self.treasureNum, self.gameName, self.userName), add="+")

        #MainMenu button
        self.m_path = "imgM.png"
        self.M_image = tk.PhotoImage(file = master.getPath(self.m_path))
        self.mimg = self.ffs.create_image(self.ffs.winfo_width()*0.32,self.ffs.winfo_height()*0.75, image= self.M_image, anchor = tk.CENTER, tag="button")
 
        self.BP_image = tk.PhotoImage(file = master.getPath("imgMP.png"))
        self.ffs.tag_bind(self.mimg, "<Enter>", lambda event: setattr(self, 'm_path', "imgMP.png"), add="+")
        self.ffs.tag_bind(self.mimg, "<Enter>", lambda event: master.resizer(master.getPath(self.m_path), self.ffs, self.mimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        self.ffs.tag_bind(self.mimg, "<Leave>", lambda event: setattr(self, 'm_path', "imgM.png"), add="+")
        self.ffs.tag_bind(self.mimg, "<Leave>", lambda event: master.resizer(master.getPath(self.m_path), self.ffs, self.mimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08)), add="+")
        self.ffs.tag_bind(self.mimg, "<Button-1>", lambda event: self.deleteCanvas(master, "HomeScreen"), add="+")
        #self.ffs.tag_bind(self.mimg, "<Button-1>", lambda event: self.loadGame(master), add="+")

        def resizeEnd(event, *args):
            master.resizer(master.getPath("transparency.png"), self.canvas, self.eimg, master.winfo_width(), master.winfo_height())
            master.resizer(master.getPath(end_file), self.ffs, self.eimg2, self.ffs.winfo_width(), self.ffs.winfo_height())
            master.resizer(master.getPath(self.pa_path), self.ffs, self.paimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08))
            master.resizer(master.getPath(self.m_path), self.ffs, self.mimg, int(master.winfo_width()*0.14), int(master.winfo_height()*0.08))
        
        resizeEnd(None)

    def deleteCanvas(self, master, name, *args, **kwargs):
        self.stopBlinking = True
        self.unbind('<Configure>')
        self.ffs.unbind_all("<Enter>")
        self.ffs.unbind_all("<Leave>")
        self.ffs.unbind_all("<Button-1>")
        self.ffs.delete('all')
        self.canvas.unbind_all("<Enter>")
        self.canvas.unbind_all("<Leave>")
        self.canvas.unbind_all("<Button-1>")
        self.canvas.delete('all')
        master.show_frame(name, *args, **kwargs)

    def alterMenu(self, master):
        master.deleteMenuBar('Menu')
        menubar = tk.Menu(master, borderwidth=0)
        fileMenu = tk.Menu(menubar, background = "#d0c4b4",fg='#2a2e2c', tearoff=False, activebackground='#c0b4ac',activeforeground='#1c1c1c', borderwidth=0, font='terminal 12', relief=tk.RAISED)
        for label, command, shortcut_text, shortcut in (
                ("Save...", lambda: self.saveGame(master), "Ctrl+S", "<Control-s>"),
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

    def saveGame(self, master, event=None):
        parser = ConfigParser()
        configFile=master.getPath(self.userName+ '#' + self.gameName + '#' + str(date.today()) +'.ini')
        ghostList = []
        for i, ghost in enumerate(self.ghosts):
            ghostList.append(ghost.save())

        parser[self.gameName] = {
            'sideLen': self.sideLen,
            'finishFactor': self.finishFac,
            'ghostFactor': self.ghostFac,
            'ghostNum': self.ghostNum,
            'treasureNum': self.treasureNum,
            'gameName': self.gameName,
            'userName': self.userName,
            'map': self.map,
            'finishX': self.finishX,
            'finishY': self.finishY,
            'startX': self.startX,
            'startY': self.startY,
            'treasuresList': self.treasuresList,
            'visitedTreasures': self.visitedTreasures,
            'shortestPath': self.shortestPath,
            'date': str(date.today()),
            'ghosts': ghostList
        }

        

        try:
            with open(configFile, 'w') as config_file:
                parser.write(config_file)
        except FileNotFoundError:
            tk.messagebox.showwarning("showwarning", "File to save game not found!") 
        except OSError:
            tk.messagebox.showwarning("showwarning", "OS error occurred trying to save game") 
        except Exception as err:
            tk.messagebox.showwarning("showwarning", "Unexpected error when saving game") 
        pass