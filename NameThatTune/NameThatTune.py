#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter,tkinter.font
import time
import os
import random
import math
import simpleaudio as sa

#Beware: what you are about to read is ugly, bloody code...

class simpleapp_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        
        ##Defining variables and arrays
        
        self.HOME = os.getcwd()
        self.songDir = os.path.join(self.HOME,'.NTT')
        if not os.path.exists(self.songDir):
            os.mkdir(self.songDir)
        self.songListFile = os.path.join(self.songDir,"SongList.txt")
        self.randomListFile = os.path.join(self.songDir,"RandomList.txt")
        self.counter = 0
        
        self.colorArray = ["red","blue","yellow","green","orange","purple","brown","pink","white","black"]
        self.textColorArray = ["white","white","black","white","black","white","white","black","black","white"]
        
        self.TeamNum = tkinter.IntVar()
        self.TeamNum.set(2)
        
        self.countdownLength = 30
        self.countUp = 0
        self.timeOut = tkinter.StringVar()
        self.timeOut.set("Time's up!")
        self.p = sa.WaveObject(b'').play()
        
        self.defaultFontSize=12
        
        self.Font = tkinter.font.Font(family="system",size=self.defaultFontSize)
        self.scoreFont = tkinter.font.Font(family="system",size=int(self.defaultFontSize*0.75))
        self.gbFont = tkinter.font.Font(family="system",size=self.defaultFontSize)
        
        self.timer=tkinter.IntVar()
        self.timer.set(self.countdownLength)
        
        ##Making the Menu
        
        self.menu = tkinter.Menu()
        self.menu.add_command(label="Launch Board",command=self.launchBoard)
        self.menu.add_command(label="Launch editor",command=self.launchEditor)
        self.config(menu=self.menu)
        
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())
        self.grid()
        
        #Creating the Control Window
        self.introLabel=tkinter.Label(self,text="Launch a new board to begin the game",font=self.Font)
        self.introLabel.grid(column=0,row=0,sticky="NSEW")
        
    
    ##Function definitions
    
    def redefineAndRandomize(self):
        with open(self.songListFile) as f:
            self.songString = f.read()
        self.songArray = self.songString.splitlines()
        self.songNumber = len(self.songArray)
        
        self.songRandom = random.sample(range(self.songNumber), self.songNumber)
        with open(self.randomListFile,'w') as self.RLF:
            self.newSongList = list(range(self.songNumber))
            for item in range(self.songNumber):
                self.newSongList[item] = self.songArray[self.songRandom[item]]
            self.RLF.writelines( "%s\n" % item for item in self.newSongList )
    
    def launchEditor(self):
        self.redefineAndRandomize()
        self.ed = tkinter.Toplevel(self)
        self.ed.total = tkinter.Label(self.ed,text="Songs in list: %s" % self.songNumber)
        self.ed.total.grid(row=0,sticky="NSEW")
        self.ed.filepath = tkinter.StringVar()
        self.ed.showName = tkinter.StringVar()
        self.ed.songName = tkinter.StringVar()
        self.ed.filepathEntry=tkinter.Entry(self.ed,textvariable=self.ed.filepath)
        self.ed.filepathEntry.grid(row=1,sticky="NSEW")
        self.ed.showNameEntry=tkinter.Entry(self.ed,textvariable=self.ed.showName)
        self.ed.showNameEntry.grid(row=2,sticky="NSEW")
        self.ed.songNameEntry=tkinter.Entry(self.ed,textvariable=self.ed.songName)
        self.ed.songNameEntry.grid(row=3,sticky="NSEW")
        self.ed.filepath.set("Enter file name here")
        self.ed.showName.set("Enter show/artist name here")
        self.ed.songName.set("Enter song name here")
        self.ed.saveNew = tkinter.Button(self.ed,text="Save",command=self.saveSong)
        self.ed.saveNew.grid(row=4,sticky="NSEW")
        self.ed.grid()
        
    def saveSong(self):
        self.ed.newAppendage = []
        if self.ed.showName.get():
            if self.ed.showName.get() != "Enter show name here":
                self.ed.newAppendage.append(self.ed.showName.get())
        if self.ed.songName.get():
            if self.ed.songName.get() != "Enter song name here":
                self.ed.newAppendage.append(self.ed.songName.get())
        if len(self.ed.newAppendage) == 2 and self.ed.filepath.get() != "Enter file name here":
            self.ed.confirm = tkinter.Toplevel(self.ed)
            self.ed.confirm.ask = tkinter.Label(self.ed.confirm,text="Add %s for the information for %s?" % (str(self.ed.newAppendage),self.ed.filepath.get()))
            self.ed.confirm.ask.grid(row=0,column=0,columnspan=2,sticky="NSEW")
            self.ed.confirm.yes = tkinter.Button(self.ed.confirm,text="Yes",command=self.saveConfirm)
            self.ed.confirm.yes.grid(row=1,column=0,sticky="NSEW")
            self.ed.confirm.no = tkinter.Button(self.ed.confirm,text="No",command=self.saveDeny)
            self.ed.confirm.no.grid(row=1,column=1,sticky="NSEW")
            self.ed.confirm.grid()
    
    def saveConfirm(self):
        with open(self.songListFile,'a') as tunes:
            tunes.write(str(self.ed.newAppendage+[self.ed.filepath.get()])+'\n')
        self.ed.filepath.set("Enter file name here")
        self.ed.showName.set("Enter show name here")
        self.ed.songName.set("Enter song name here")
        self.redefineAndRandomize()
        self.ed.total.config(text="Songs in list: %s" % self.songNumber)
        self.ed.confirm.destroy()
        
    def saveDeny(self):
        self.ed.confirm.destroy()
        
    def autoSize(self):
        scale=35
        self.ws = self.winfo_width()
        self.Font.config(size=int(math.ceil(self.ws/scale)))
        self.scoreFont.config(size=int(math.ceil(self.ws/scale*0.75)))
        self.gb.ws = self.gb.winfo_width()
        self.gbFont.config(size=int(math.ceil(self.gb.ws/scale)))
    
    def launchBoard(self):
        self.menu.add_command(label="Auto-adjust font size",command=self.autoSize)
        self.menu.delete(1,2)
        self.menu.team = tkinter.Menu(self,tearoff=0)
        for i in range(1,11):
            exec('def changeTo'+str(i)+'():'+
                '\n    app.TeamNum.set('+str(i)+')'+
                '\n    app.updateTeam()')
            exec('self.menu.team.add_command(label="'+str(i)+'",command=changeTo'+str(i)+')')
        self.menu.add_cascade(label="Number of Teams",menu=self.menu.team)
        self.menu.navi = tkinter.Menu(self,tearoff=0)
        self.menu.navi.add_command(label="Skip",command=self.skipIt)
        self.menu.navi.add_command(label="Previous",command=self.goBack)
        self.menu.navi.add_command(label="Play this song",command=self.playsnip)
        self.menu.add_cascade(label="Navigation",menu=self.menu.navi)
        self.changeControlBoard()
        
        self.gb = tkinter.Toplevel(self)
        self.gb.info = tkinter.Frame(self.gb)
        self.gb.info.grid(row=0,sticky="NSEW")
        self.songsRemaining = tkinter.StringVar()
        self.songsRemaining.set("Songs left: %r" % self.songNumber)
        self.gb.info.remaining = tkinter.Label(self.gb.info,bg="#dddddd",textvariable=self.songsRemaining,relief="sunken",font=self.gbFont)
        self.gb.info.remaining.grid(row=0,column=0,sticky="NSEW")
        self.gb.info.clock = tkinter.Label(self.gb.info,bg="#dddddd",textvariable=self.timer,relief="sunken",font=self.gbFont)
        self.gb.info.clock.grid(row=0,column=1,sticky="NSEW")
        for i,thing in enumerate(["Show","Song"]):
            exec('self.gb.info.'+thing+' = tkinter.Label(self.gb.info,bg="black",textvariable=self.current'+thing+',font=self.gbFont)')
            exec('self.gb.info.'+thing+'.grid(row='+str(i+1)+',column=0,columnspan=2,sticky="NSEW")')
        self.gb.info.rowconfigure(0,weight=1)
        self.gb.info.rowconfigure(1,weight=4)
        self.gb.info.rowconfigure(2,weight=4)
        self.gb.info.columnconfigure(0,weight=1)
        self.gb.info.columnconfigure(1,weight=1)
        
        self.gb.team = tkinter.Frame(self.gb)
        self.gb.team.grid(row=1,sticky="NSEW")
        for i in range(1,11):
            exec('app.team'+str(i)+'=tkinter.IntVar()')
            for op in ["+","-"]:
                if op == "+":
                    oper="Add"
                else:
                    oper="Sub"
                exec('def team'+str(i)+oper+'point():'+
                    '\n    app.team'+str(i)+'.set(eval(str(app.team'+str(i)+'.get())+"'+op+'1"))')
                exec('app.team'+str(i)+oper+'Butt=tkinter.Button(self.team,bg=self.colorArray['+str(i-1)+'],fg=self.textColorArray['+str(i-1)+'],text="'+oper+'",command=team'+str(i)+oper+'point,font=self.scoreFont)')
            exec('app.gb.team.team'+str(i)+'lab=tkinter.Label(self.gb.team,bg=self.colorArray['+str(i-1)+'],fg=self.textColorArray['+str(i-1)+'],textvariable=self.team'+str(i)+',font=self.gbFont)')
            exec('app.team'+str(i)+'lab=tkinter.Label(self.team,bg=self.colorArray['+str(i-1)+'],fg=self.textColorArray['+str(i-1)+'],textvariable=self.team'+str(i)+',font=self.scoreFont)')
            
            
        self.gb.team.rowconfigure(0,weight=1)
        self.gb.columnconfigure(0,weight=1)
        self.gb.rowconfigure(0,weight=7)
        self.gb.rowconfigure(1,weight=1)
        
        self.updateTeam()
        self.gb.resizable(True,True)
        self.gb.update()
        self.gb.geometry(self.gb.geometry())
        self.gb.grid()
        
    def changeControlBoard(self):
        self.introLabel.grid_remove()
        self.info = tkinter.Frame(self)
        self.info.grid(row=0,column=0,columnspan=3,sticky="NSEW")
        self.team = tkinter.Frame(self)
        self.team.grid(row=1,sticky="NSEW")
        self.PlayButt = tkinter.Button(self,text="Play song",command=self.beginCountdown,font=self.Font)
        self.PlayButt.grid(row=1,column=1,sticky="NSEW")
        self.clock = tkinter.Label(self,bg="#dddddd",textvariable=self.timer,relief="sunken",font=self.gbFont)
        self.clock.grid(row=1,column=2,sticky="NSEW")
        for thing in ["row","column"]:
            for i in [0,1]:
                exec('self.'+thing+'configure('+str(i)+',weight=1)')
        self.redefineAndRandomize()
        for i,thing in enumerate(["Show","Song"]):
            exec('self.current'+thing+'=tkinter.StringVar()')
            exec('self.current'+thing+'.set(eval(self.newSongList[0])['+str(i)+'])')
            exec('self.info.'+thing+' = tkinter.Label(self.info,textvariable=self.current'+thing+',font=self.Font,relief="sunken")')
            exec('self.info.'+thing+'.grid(row='+str(i)+',column=0,sticky="NSEW")')
            exec('def reveal'+thing+'():'+
                '\n    app.gb.palette = ["f","d","b"]'+
                '\n    app.gb.bg = "#"'+
                '\n    for i in range(6):'+
                '\n        app.gb.bg = app.gb.bg + app.gb.palette[int(random.random()*3)-1]'+
                '\n    if  app.info.reveal'+thing+'Butt.config("relief")[-1] == "raised":'+
                '\n        app.gb.info.'+thing+'.config(bg=app.gb.bg)'+
                '\n        app.info.reveal'+thing+'Butt.config(relief="sunken",text="Hide")'
                '\n    else:'
                '\n        app.gb.info.'+thing+'.config(bg="#000000")'+
                '\n        app.info.reveal'+thing+'Butt.config(relief="raised",text="Reveal")')
            exec('self.info.reveal'+thing+'Butt = tkinter.Button(self.info,state="disabled",text="Reveal",command=reveal'+thing+',font=self.Font)')
            exec('self.info.reveal'+thing+'Butt.grid(row='+str(i)+',column=1,sticky="NSEW")')
        for thing in ["row","column"]:
            for i in [0,1]:
                exec('self.info.'+thing+'configure('+str(i)+',weight=1)')
        for i in range(0,3):
            exec('self.team.rowconfigure('+str(i)+',weight=1)')
    
    def updateTeam(self):
        for i in range(1,11):
            if i <= self.TeamNum.get():
                exec('app.gb.team.team'+str(i)+'lab.grid(column='+str(i-1)+',row=0,sticky="NSEW")')
                exec('app.gb.team.columnconfigure('+str(i-1)+',weight=1)')
                exec('app.team'+str(i)+'lab.grid(column='+str(i-1)+',row=1,sticky="NSEW")')
                exec('app.team'+str(i)+'AddButt.grid(column='+str(i-1)+',row=0,sticky="NSEW")')
                exec('app.team'+str(i)+'SubButt.grid(column='+str(i-1)+',row=2,sticky="NSEW")')
                exec('app.team.columnconfigure('+str(i-1)+',weight=1)')
            else:
                exec('app.gb.team.team'+str(i)+'lab.grid_remove()')
                exec('app.gb.team.columnconfigure('+str(i-1)+',weight=0)')
                exec('app.team'+str(i)+'lab.grid_remove()')
                exec('app.team'+str(i)+'AddButt.grid_remove()')
                exec('app.team'+str(i)+'SubButt.grid_remove()')
                exec('app.team.columnconfigure('+str(i-1)+',weight=0)')
    
    def beginCountdown(self):
        if self.PlayButt.config("relief")[-1]=="sunken":
            self.skipIt()
            self.p.stop()
            self.ongoingTimer = False
        else:
            self.PlayButt.config(relief="sunken",text="Reset")
            self.playsnip()
            self.ongoingTimer = True
            self.countdown(self.currentSong.get())
            self.info.revealShowButt.config(state="normal")
            self.info.revealSongButt.config(state="normal")
    
    def skipIt(self):
        if self.songNumber > 0:
            if self.p.is_playing():
                self.p.stop()
            self.countUp=self.countUp+1
            self.songNumber=self.songNumber-1
            self.updateCells()
            
    
    def goBack(self):
        if self.songNumber < len(self.songArray):
            if self.p.is_playing():
                self.p.stop()
            self.countUp=self.countUp-1
            self.songNumber=self.songNumber+1
            self.updateCells()
    
    def updateCells(self):
        self.ongoingTimer = False
        self.PlayButt.config(relief="raised",text="Play song")
        self.songsRemaining.set("Songs left: %r" % self.songNumber)
        self.gb.info.Show.config(bg="black")
        self.gb.info.Song.config(bg="black")
        self.currentShow.set(eval(self.newSongList[self.countUp])[0])
        self.currentSong.set(eval(self.newSongList[self.countUp])[1])
        self.timer.set(self.countdownLength)
        self.gb.info.clock.config(textvariable=self.timer)
        self.info.revealShowButt.config(relief="raised",text="Reveal",state="disabled")
        self.info.revealSongButt.config(relief="raised",text="Reveal",state="disabled")
    
    def countdown(self,NP):
        if self.p.is_playing():
            self.after(100,self.countdown,NP)
        elif self.ongoingTimer and NP == self.currentSong.get():
            if self.timer.get() > 0:
                self.timer.set(self.timer.get()-1)
                self.after(1000,self.countdown,NP)
            else:
                self.ongoingTimer = False
                self.gb.info.clock.config(textvariable=self.timeOut)
            
    def playsnip(self):
        self.p = sa.WaveObject.from_wave_file(os.path.join(self.songDir,eval(self.newSongList[self.countUp])[2]))
        self.p = self.p.play()
        
if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Python ConGames --> Name That Tune!')
    app.mainloop()
