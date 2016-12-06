#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter,tkFont
import time
import os
import random
import math

#Beware: what you are about to read is ugly, bloody code...

class simpleapp_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		
	def initialize(self):
		
		##Defining variables and arrays
		
		self.HOME = os.getcwd()
		if not os.path.exists(self.HOME+'/.NTT'):
			os.mkdir(self.HOME+'/.NTT')
		self.songListFile = "%s/.NTT/SongList.txt" % self.HOME
		self.randomListFile = "%s/.NTT/RandomList.txt" % self.HOME
		
		self.colorArray = ["red","blue","yellow","green","orange","purple","brown","pink","white","black"]
		self.textColorArray = ["white","white","black","white","black","white","white","black","black","white"]
		
		self.TeamNum = Tkinter.IntVar()
		self.TeamNum.set(1)
		
		self.countdownLength = 20
		self.countUp = 0
		self.timeOut = Tkinter.StringVar()
		self.timeOut.set("Time's up!")
		
		self.defaultFontSize=12
		
		self.Font = tkFont.Font(family="system",size=self.defaultFontSize)
		self.scoreFont = tkFont.Font(family="system",size=int(self.defaultFontSize*0.75))
		self.gbFont = tkFont.Font(family="system",size=self.defaultFontSize)
		
		##Making the Menu
		
		self.menu = Tkinter.Menu()
		self.menu.add_command(label="Auto-adjust font size",command=self.autoSize)
		self.menu.add_command(label="Launch Board",command=self.launchBoard)
		self.menu.add_command(label="Launch editor",command=self.launchEditor)
		self.config(menu=self.menu)
		
		self.resizable(True,True)
		self.update()
		self.geometry(self.geometry())
		self.grid()
		
		#Creating the Control Window
		self.introLabel=Tkinter.Label(self,text="Launch a new board to begin the game",font=self.Font)
		self.introLabel.grid(column=0,row=0,sticky="NSEW")
		
	
	##Function definitions
	
	def redefineAndRandomize(self):
		self.songString = open(self.songListFile).read()
		self.songArray = self.songString.splitlines()
		self.songNumber = len(self.songArray)
		
		self.songRandom = random.sample(range(self.songNumber), self.songNumber)
		with open(self.randomListFile,'w') as self.RLF:
			self.newSongList = range(self.songNumber)
			for item in range(self.songNumber):
				self.newSongList[item] = self.songArray[self.songRandom[item]]
			self.RLF.writelines( "%s\n" % item for item in self.newSongList )
	
	def launchEditor(self):
		self.redefineAndRandomize()
		self.ed = Tkinter.Toplevel(self)
		self.ed.total = Tkinter.Label(self.ed,text="Songs in list: %s" % self.songNumber)
		self.ed.total.grid(row=0,sticky="NSEW")
		self.ed.showName = Tkinter.StringVar()
		self.ed.songName = Tkinter.StringVar()
		self.ed.showNameEntry=Tkinter.Entry(self.ed,textvariable=self.ed.showName)
		self.ed.showNameEntry.grid(row=1,sticky="NSEW")
		self.ed.songNameEntry=Tkinter.Entry(self.ed,textvariable=self.ed.songName)
		self.ed.songNameEntry.grid(row=2,sticky="NSEW")
		self.ed.showName.set("Enter show name here")
		self.ed.songName.set("Enter song name here")
		self.ed.saveNew = Tkinter.Button(self.ed,text="Save",command=self.saveSong)
		self.ed.saveNew.grid(row=3,sticky="NSEW")
		self.ed.grid()
		
	def saveSong(self):
		self.ed.newAppendage = []
		if self.ed.showName.get():
			if self.ed.showName.get() != "Enter show name here":
				self.ed.newAppendage.append(self.ed.showName.get())
		if self.ed.songName.get():
			if self.ed.songName.get() != "Enter song name here":
				self.ed.newAppendage.append(self.ed.songName.get())
		if len(self.ed.newAppendage) == 2:
			self.ed.confirm = Tkinter.Toplevel(self.ed)
			self.ed.confirm.ask = Tkinter.Label(self.ed.confirm,text="Add %s for the information for %s.mp3?" % (str(self.ed.newAppendage),self.songNumber+1))
			self.ed.confirm.ask.grid(row=0,column=0,columnspan=2,sticky="NSEW")
			self.ed.confirm.yes = Tkinter.Button(self.ed.confirm,text="Yes",command=self.saveConfirm)
			self.ed.confirm.yes.grid(row=1,column=0,sticky="NSEW")
			self.ed.confirm.no = Tkinter.Button(self.ed.confirm,text="No",command=self.saveDeny)
			self.ed.confirm.no.grid(row=1,column=1,sticky="NSEW")
			self.ed.confirm.grid()
	
	def saveConfirm(self):
		self.ed.tunes = open(self.songListFile,'a')
		self.ed.tunes.write(str(self.ed.newAppendage)+'\n')
		self.ed.tunes.close()
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
		self.menu.delete(2,3)
		self.menu.team = Tkinter.Menu(self,tearoff=0)
		for i in range(1,11):
			exec('def changeTo'+str(i)+'():'+
				'\n    app.TeamNum.set('+str(i)+')'+
				'\n    app.updateTeam()')
			exec('self.menu.team.add_command(label="'+str(i)+'",command=changeTo'+str(i)+')')
		self.menu.add_cascade(label="Number of Teams",menu=self.menu.team)
		self.changeControlBoard()
		self.timer=Tkinter.IntVar()
		self.timer.set(self.countdownLength)
		
		self.gb = Tkinter.Toplevel(self)
		self.gb.info = Tkinter.Frame(self.gb)
		self.gb.info.grid(row=0,sticky="NSEW")
		self.songsRemaining = Tkinter.StringVar()
		self.songsRemaining.set("Songs left: %r" % self.songNumber)
		self.gb.info.remaining = Tkinter.Label(self.gb.info,bg="#dddddd",textvariable=self.songsRemaining,relief="sunken",font=self.gbFont)
		self.gb.info.remaining.grid(row=0,column=0,sticky="NSEW")
		self.gb.info.clock = Tkinter.Label(self.gb.info,bg="#dddddd",textvariable=self.timer,relief="sunken",font=self.gbFont)
		self.gb.info.clock.grid(row=0,column=1,sticky="NSEW")
		for i,thing in enumerate(["Show","Song"]):
			exec('self.gb.info.'+thing+' = Tkinter.Label(self.gb.info,bg="black",textvariable=self.current'+thing+',font=self.gbFont)')
			exec('self.gb.info.'+thing+'.grid(row='+str(i+1)+',column=0,columnspan=2,sticky="NSEW")')
		self.gb.info.rowconfigure(0,weight=1)
		self.gb.info.rowconfigure(1,weight=4)
		self.gb.info.rowconfigure(2,weight=4)
		self.gb.info.columnconfigure(0,weight=1)
		self.gb.info.columnconfigure(1,weight=1)
		
		self.gb.team = Tkinter.Frame(self.gb)
		self.gb.team.grid(row=1,sticky="NSEW")
		for i in range(1,11):
			exec('app.team'+str(i)+'=Tkinter.IntVar()')
			for op in ["+","-"]:
				if op == "+":
					oper="Add"
				else:
					oper="Sub"
				exec('def team'+str(i)+oper+'point():'+
					'\n    app.team'+str(i)+'.set(eval(str(app.team'+str(i)+'.get())+"'+op+'1"))')
				exec('app.team'+str(i)+oper+'Butt=Tkinter.Button(self.team,bg=self.colorArray['+str(i-1)+'],fg=self.textColorArray['+str(i-1)+'],text="'+oper+'",command=team'+str(i)+oper+'point,font=self.scoreFont)')
			exec('app.gb.team.team'+str(i)+'lab=Tkinter.Label(self.gb.team,bg=self.colorArray['+str(i-1)+'],fg=self.textColorArray['+str(i-1)+'],textvariable=self.team'+str(i)+',font=self.gbFont)')
			exec('app.team'+str(i)+'lab=Tkinter.Label(self.team,bg=self.colorArray['+str(i-1)+'],fg=self.textColorArray['+str(i-1)+'],textvariable=self.team'+str(i)+',font=self.scoreFont)')
			
			
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
		self.info = Tkinter.Frame(self)
		self.info.grid(row=0,column=0,columnspan=2,sticky="NSEW")
		self.team = Tkinter.Frame(self)
		self.team.grid(row=1,sticky="NSEW")
		self.PlayButt = Tkinter.Button(self,text="Play song",command=self.beginCountdown,font=self.Font)
		self.PlayButt.grid(row=1,column=1,sticky="NSEW")
		for thing in ["row","column"]:
			for i in [0,1]:
				exec('self.'+thing+'configure('+str(i)+',weight=1)')
		self.redefineAndRandomize()
		for i,thing in enumerate(["Show","Song"]):
			exec('self.current'+thing+'=Tkinter.StringVar()')
			exec('self.current'+thing+'.set(str(eval(self.newSongList[0])['+str(i)+']))')
			exec('self.info.'+thing+' = Tkinter.Label(self.info,textvariable=self.current'+thing+',font=self.Font,relief="sunken")')
			exec('self.info.'+thing+'.grid(row='+str(i)+',column=0,sticky="NSEW")')
			exec('def reveal'+thing+'():'+
				'\n    if  app.info.reveal'+thing+'Butt.config("relief")[-1] == "raised":'+
				'\n        app.gb.info.'+thing+'.config(bg="#dddddd")'+
				'\n        app.info.reveal'+thing+'Butt.config(relief="sunken",text="Hide")'
				'\n    else:'
				'\n        app.gb.info.'+thing+'.config(bg="#000000")'+
				'\n        app.info.reveal'+thing+'Butt.config(relief="raised",text="Reveal")')
			exec('self.info.reveal'+thing+'Butt = Tkinter.Button(self.info,state="disabled",text="Reveal",command=reveal'+thing+',font=self.Font)')
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
			self.ongoingTimer = False
			self.PlayButt.config(relief="raised",text="Play song")
			self.songsRemaining.set("Songs left: %r" % self.songNumber)
			self.gb.info.Show.config(bg="black")
			self.gb.info.Song.config(bg="black")
			self.currentShow.set(str(eval(self.newSongList[self.countUp])[0]))
			self.currentSong.set(str(eval(self.newSongList[self.countUp])[1]))
			self.timer.set(self.countdownLength)
			self.gb.info.clock.config(textvariable=self.timer)
			self.info.revealShowButt.config(relief="raised",text="Reveal",state="disabled")
			self.info.revealSongButt.config(relief="raised",text="Reveal",state="disabled")
		else:
			self.PlayButt.config(relief="sunken",text="Reset")
			self.playsnip()
			self.ongoingTimer = True
			self.countdown()
			self.info.revealShowButt.config(state="normal")
			self.info.revealSongButt.config(state="normal")
	
	def countdown(self):
		if self.ongoingTimer:
			if self.timer.get() > 0:
				self.timer.set(self.timer.get()-1)
				self.after(1000,self.countdown)
			else:
				self.ongoingTimer = False
				self.gb.info.clock.config(textvariable=self.timeOut)
			
	def playsnip(self):
		self.countUp=self.countUp+1
		os.system("cvlc --play-and-exit --no-repeat --no-loop "+self.HOME+"/.NTT/"+str(self.songRandom[self.countUp-1]+1)+".mp3")
		self.songNumber=self.songNumber-1
		
if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title('Python ConGames --> Name That Tune!')
	app.mainloop()
