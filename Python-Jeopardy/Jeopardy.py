#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter,tkFont
from PIL import Image, ImageTk
import os
import time
import math
import glob

class simpleapp_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		
	def initialize(self):
		self.HOME = os.getcwd()
		if not os.path.exists(self.HOME+'/.PythonJeopardy'):
			os.mkdir(self.HOME+'/.PythonJeopardy')

		if not os.path.exists(self.HOME+'/.PythonJeopardy/Default'):
			f=open(self.HOME+'/.PythonJeopardy/Default','w')
			ABP=[]
			for i,cat in enumerate(["Category 1","Category 2","Category 3","Category 4","Category 5"]):
				for ques in range(1,6):
					exec('q="A question"')
					exec('a="An Answer"')
					exec('i=""')
					exec('B'+str(ques)+'=[q,a,i]')
				exec('C'+str(i)+'=[B1,B2,B3,B4,B5]')
				exec('ABP.append(["'+cat+'",C'+str(i)+'])')
			P=[100,200,300,400,500]
			board = [ABP,P]
			f.write(str(board)+'\n')
			for i,item in enumerate(P):
				P[i]=item*2
			board = [ABP,P]
			f.write(str(board)+'\n')
			f.write('["A Category","A Question","An Answer",""]')
			f.close()
		self.OpenFile = self.HOME+"/.PythonJeopardy/Default"
		self.PTS=0
					
		if not os.path.exists(self.HOME+'/.PythonJeopardy/DefaultSettings.cfg'):
			f=open(self.HOME+'/.PythonJeopardy/DefaultSettings.cfg','w')
			self.NP,self.PC,self.CC=True,True,True
			f.write("["+str(self.NP)+","+str(self.PC)+","+str(self.CC)+"]")
		else:
			f=open(self.HOME+'/.PythonJeopardy/DefaultSettings.cfg','r')
			self.NP,self.PC,self.CC = eval(str(f.read()))
		
		self.menya = Tkinter.Menu(self)
		self.OpenMenu = Tkinter.Menu(self.menya,tearoff=0)
		for i,name in enumerate(glob.glob(self.HOME+'/.PythonJeopardy/*.board')):
			if name:
				exec('def Open'+str(i)+'():'+
					'\n    app.OpenFile ="'+name+'"'+
					'\n    app.arrayload()')
				exec('self.OpenMenu.add_command(label="'+name+'", command=Open'+str(i)+')')
			else:
				self.OpenMenu.add_command(label="{None Found}")
		self.menya.Round = Tkinter.Menu(self.menya,tearoff=0)
		for Round in [1,2,3]:
			exec('self.menya.Round.add_command(label="Round '+str(Round)+'",command=self.loadround'+str(Round)+')')
		self.menya.add_cascade(label="Open",menu=self.OpenMenu)
		self.menya.add_command(label="Settings",command=self.changeSets)
		self.menya.add_cascade(label="Round",menu=self.menya.Round)
		self.menya.add_command(label="Auto Font Size",command=self.fontadj)
		self.config(menu=self.menya)
		
		self.Font = tkFont.Font(family="system",size=12)
		self.scoreFont = tkFont.Font(family="system",size=8)
		
		################################################################
		#						   Score&Time						   #
		################################################################
		
		self.ScoreTime = Tkinter.Frame(self)
		self.ScoreTime.grid(column=0,row=1,sticky="NSEW")
		
		self.ScoreTime.timeOut = Tkinter.StringVar()
		self.ScoreTime.timeOut.set("Time's up!")
		
		self.ScoreTime.timeValue = Tkinter.IntVar()
				
		################################################################
		#						   Game Board						   #
		################################################################
		self.gb = Tkinter.Frame(self)
		
		for cat in range(0,5):
			exec('self.gb.catlab'+str(cat)+' = Tkinter.Label(self.gb,wraplength=100,font=self.Font,width='+str(self.winfo_width()/5)+',relief="raised",bg="white")')
			exec('self.gb.catlab'+str(cat)+'.grid(column='+str(cat)+',row=0,sticky="NSEW")')
			for ques in range(1,6):
				exec('self.gb.box'+str(cat)+'x'+str(ques)+' = Tkinter.Button(self.gb,command=self.reveal'+str(cat)+'x'+str(ques)+',font=self.Font,width='+str(self.winfo_width()/5)+')')
				exec('self.gb.box'+str(cat)+'x'+str(ques)+'.grid(column='+str(cat)+',row='+str(ques)+',sticky="NSEW")')
		self.Round = 1
		
		for i in range(0,6):
			if i<5:
				exec('self.gb.grid_columnconfigure('+str(i)+',weight=1)')
			exec('self.gb.grid_rowconfigure('+str(i)+',weight=1)')
			
		################################################################
		#                           Building                           #
		################################################################
		
		self.arrayload()
		
		self.ScoreTime.Clock = Tkinter.Frame(self.ScoreTime)
		for i in range(0,3):
			self.ScoreTime.Clock.grid_rowconfigure(i,weight=1)
		self.ScoreTime.Clock.grid_columnconfigure(0,weight=1)
		
		self.ScoreTime.Clock.button_ST = Tkinter.Button(self.ScoreTime.Clock, text=u"Start Clock",command=self.startClock, relief="raised",font=self.scoreFont)
		self.ScoreTime.Clock.timeEntry = Tkinter.Entry(self.ScoreTime.Clock,textvariable=self.ScoreTime.timeValue,font=self.scoreFont,width=0)
		
		self.ScoreTime.Clock.timeCountdown = Tkinter.IntVar()
		self.ScoreTime.Clock.labelTime = Tkinter.Label(self.ScoreTime.Clock,textvariable=self.ScoreTime.Clock.timeCountdown,font=self.Font)
		
		self.ScoreTime.Clock.timeCountdown.set(self.ScoreTime.timeValue.get())
		
		self.ScoreTime.Clock.timerStart = Tkinter.BooleanVar()
		self.ScoreTime.Clock.timerStart.set(False)
		
		self.clockDecision()
		
		self.playerDecision()
		
		self.pointDecision()
		
		################################################################
		#                           Geometry                           #
		################################################################
		
		self.grid_rowconfigure(0,weight=1)
		self.grid_rowconfigure(1,weight=0)
		self.grid_columnconfigure(0,weight=1)
		self.resizable(True,True)
		self.update()
		self.geometry(self.geometry())
		self.grid()
	
	####################################################################
	#							  Definitions						   #
	####################################################################
		
	for Round in [1,2,3]:
		exec('def loadround'+str(Round)+'(self):'+
			'\n    self.Round = '+str(Round)+
			'\n    self.gb.grid_remove()'+
			'\n    self.arrayload()'+
			'\n    self.iHateYouTkInter()')
	
	def arrayload(self):
		f=open(self.OpenFile,'r')
		sepf = f.readlines()
		self.clusterfuck = {}
		self.clusterfuck = eval(str(sepf[self.Round-1]))
		if self.Round <3:
			self.P=eval(str(self.clusterfuck[1]))
			self.gb.grid(column=0,row=0,sticky="NSEW")
			self.ScoreTime.timeValue.set(20)
			for cat in range(0,5):
				exec('self.gb.catlab'+str(cat)+'.config(text="'+str(eval(str(eval(str(self.clusterfuck[0]))[cat]))[0])+'")')
				for ques in range(1,6):
					exec('self.gb.box'+str(cat)+'x'+str(ques)+'.config(text=str(eval(str(self.clusterfuck[1]))['+str(ques-1)+']),state="normal")')
		else:
			self.FinalJep = Tkinter.Frame(self)
			self.ScoreTime.timeValue.set(60)
			self.FinalJep.CatLab = Tkinter.Button(self.FinalJep,text=self.clusterfuck[0],font=self.Font,command=self.FinalQ,wraplength=self.winfo_width())
			self.FinalJep.CatLab.grid(sticky="NSEW")
			self.FinalJep.grid(row=0,column=0,sticky="NSEW")
			self.FinalJep.rowconfigure(0,weight=1)
			self.FinalJep.columnconfigure(0,weight=1)
		f.close()
	
	def FinalQ(self):
		self.FinalJep.CatLab.grid_remove()
		self.FinalJep.QuesLab = Tkinter.Label(self.FinalJep,text=self.clusterfuck[1],font=self.Font,wraplength=self.winfo_width())
		self.FinalJep.QuesLab.grid(row=0,sticky="NSEW")
		self.FinalJep.Proceed = Tkinter.Button(self.FinalJep,text="Reveal",command=self.endgame,font=self.Font)
		self.FinalJep.Proceed.grid(row=1,sticky="NSEW")
		if not self.CC:
			self.startClock()
	
	def endgame(self):
		self.FinalJep.QuesLab.grid_remove()
		self.FinalJep.Proceed.grid_remove()
		self.FinalJep.Answer = Tkinter.Label(self.FinalJep,text=self.clusterfuck[2],font=self.Font,wraplength=self.winfo_width())
		self.FinalJep.Answer.grid(row=0,sticky="NSEW")
		self.FinalJep.NewGame = Tkinter.Button(self.FinalJep,text="Start a new game",command=self.resetIt,font=self.Font)
		self.FinalJep.NewGame.grid(row=1,sticky="NSEW")
		if not self.CC:
			self.startClock()
		
	def resetIt(self):
		self.FinalJep.grid_remove()
		self.OpenFile = self.HOME+"/.PythonJeopardy/Default"
		self.Round = 1
		self.arrayload()
	
	def startClock(self):
		if self.ScoreTime.Clock.button_ST.config('relief')[-1] == "sunken":
			self.ScoreTime.Clock.button_ST.config(relief="raised",text="Start Clock")
			self.ScoreTime.Clock.timerStart.set(False)
			self.ScoreTime.Clock.timeCountdown.set(self.ScoreTime.timeValue.get())
			self.ScoreTime.Clock.labelTime.config(textvariable=self.ScoreTime.Clock.timeCountdown)
		else:
			self.ScoreTime.Clock.button_ST.config(relief="sunken",text="Reset Clock")
			self.ScoreTime.Clock.timeCountdown.set(self.ScoreTime.timeValue.get())
			self.ScoreTime.Clock.timerStart.set(True)
			self.countdown()
	
	def countdown(self):
		if self.ScoreTime.Clock.timerStart.get():
			if self.ScoreTime.Clock.timeCountdown.get()>0:
				self.ScoreTime.Clock.timeCountdown.set(self.ScoreTime.Clock.timeCountdown.get()-1)
				self.ScoreTime.after(1000,self.countdown)
			else:
				self.ScoreTime.Clock.labelTime.config(textvariable=self.ScoreTime.timeOut)
				self.ScoreTime.Clock.timerStart.set(False)
	
	for cat in range(0,5):
		for ques in range(1,6):
			exec('def reveal'+str(cat)+'x'+str(ques)+'(self):'+
				'\n    self.CAT='+str(cat)+
				'\n    self.QUES='+str(ques)+
				'\n    self.PTS=str(eval(str(self.clusterfuck[1]))['+str(ques-1)+'])'+
				'\n    self.reveal()')
	
	def reveal(self):
		exec('self.gb.box'+str(self.CAT)+'x'+str(self.QUES)+'.config(state="disabled")')
		self.qna = Tkinter.Frame(self)
		self.qna.pointlabel=Tkinter.Label(self.qna,text=self.PTS,font=self.Font)
		self.qna.pointlabel.grid(row=0,sticky="NSEW")
		if eval('str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))[self.CAT]))[1]))[self.QUES-1]))[2])'):
			self.qna.path=Image.open(str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))[self.CAT]))[1]))[self.QUES-1]))[2]))
			imgwidth, imgheight=self.qna.path.size
			for dim in ["width","height"]:
				scaleheight=self.gb.winfo_height()/10*7
				scalewidth=self.gb.winfo_width()-int(math.ceil(self.winfo_width()/68))
				exec('if img'+dim+'>scale'+dim+':'+
					'\n    scale=float(scale'+dim+')/img'+dim+
					'\n    newh = int(math.ceil(imgheight*scale))'+
					'\n    neww = int(math.ceil(imgwidth*scale))'+
					'\n    self.qna.path = self.qna.path.resize((neww,newh),Image.ANTIALIAS)')
			self.qna.image=ImageTk.PhotoImage(self.qna.path)
			self.qna.img=Tkinter.Label(self.qna,image=self.qna.image)
			self.qna.img.grid(row=1,sticky="NSEW")
			if eval('str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))[self.CAT]))[1]))[self.QUES-1]))[0])'):
				totrow=4
				self.qna.question=Tkinter.Label(self.qna,text=str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))[self.CAT]))[1]))[self.QUES-1]))[0]),wraplength=self.winfo_width()-int(math.ceil(self.winfo_width()/68)),font=self.Font)
				self.qna.question.grid(row=2,sticky="NSEW")
			else:
				totrow=3
		else:
			totrow=3
			self.qna.question=Tkinter.Label(self.qna,text=str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))[self.CAT]))[1]))[self.QUES-1]))[0]),wraplength=self.winfo_width()-int(math.ceil(self.winfo_width()/68)),font=self.Font)
			self.qna.question.grid(row=1,sticky="NSEW")
		self.qna.flip=Tkinter.Button(self.qna,text="Reveal",command=self.showans,font=self.Font)
		self.qna.flip.grid(row=totrow-1,sticky="NSEW")
		for i in range(0,totrow):
			if i == totrow-1:
				self.qna.rowconfigure(i,weight=0)
			elif i == 0:
				self.qna.rowconfigure(i,weight=0)
			else:
				self.qna.rowconfigure(i,weight=1)
		self.qna.columnconfigure(0,weight=1)
		self.gb.grid_remove()
		self.qna.grid(column=0,row=0,sticky="NSEW")
		if not self.CC:
			self.startClock()
	
	def showans(self):
		self.qna.grid_remove()
		self.ans = Tkinter.Frame(self)
		self.ans.pointlabel=Tkinter.Label(self.ans,text=self.PTS,font=self.Font)
		self.ans.pointlabel.grid(row=0,sticky="NSEW")
		self.ans.answer=Tkinter.Label(self.ans,text=str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))[self.CAT]))[1]))[self.QUES-1]))[1]),wraplength=self.winfo_width()-int(math.ceil(self.winfo_width()/68)),font=self.Font)
		self.ans.answer.grid(row=1,sticky="NSEW")
		self.ans.returnbtn=Tkinter.Button(self.ans,text="Return to Board",command=self.returntoboard,font=self.Font)
		self.ans.returnbtn.grid(row=2,sticky="NSEW")
		self.ans.columnconfigure(0,weight=1)
		self.ans.rowconfigure(0,weight=0)
		self.ans.rowconfigure(1,weight=1)
		self.ans.rowconfigure(2,weight=0)
		self.ans.grid(column=0,row=0,sticky="NSEW")
		if not self.CC:
			self.startClock()
		
	def returntoboard(self):
		self.ans.grid_remove()
		self.gb.grid(column=0,row=0,sticky="NSEW")

	def fontadj(self):
		ws=self.winfo_width()
		self.Font.config(size=int(math.ceil(ws/68)))
		self.scoreFont.config(size=int(math.ceil(ws/102)))
		for cat in range(0,5):
			for ques in range(1,6):
				exec('self.gb.catlab'+str(cat)+'.config(wraplength='+str(int(math.ceil(ws/5)))+',width='+str(int(math.ceil(ws/5)))+')')
				exec('self.gb.box'+str(cat)+'x'+str(ques)+'.config(wraplength='+str(int(math.ceil(ws/5)))+')')
		for name in self.ScoreTime.Teams:
			exec('self.ScoreTime.'+name+'Frame.'+name+'Entry.config(width=int(math.ceil(ws/500)))')
		self.ScoreTime.Clock.timeEntry.config(width=int(math.ceil(ws/500)))
	
	def changeSets(self):
		self.sw = Tkinter.Toplevel(self)
		i=0
		for V,S,T,F in [("NP","The game will be played with","two teams","three players"),("PC","Points will be awarded as","custom point values","full point values only"),("CC","The clock will be","manually started","started automatically")]:
			exec('def toggle'+V+'():'+
				'\n    if app.sw.'+V+'butt.config("relief")[-1] == "raised":'+
				'\n        app.sw.'+V+'butt.config(relief="sunken",text="'+F+'")'+
				'\n    else:'+
				'\n        app.sw.'+V+'butt.config(relief="raised",text="'+T+'")'+
				'\n    app.'+V+' = not app.'+V)
			exec('self.sw.'+V+'butt = Tkinter.Button(self.sw,command=toggle'+V+')')
			exec('if self.'+V+':'+
				'\n    self.sw.'+V+'butt.config(relief="raised",text="'+T+'")'+
				'\nelse:'+
				'\n    self.sw.'+V+'butt.config(relief="sunken",text="'+F+'")')
			exec('self.sw.'+V+'butt.grid(row='+str(i)+',column=1,sticky="NSEW")')
			exec('self.sw.'+V+'lab = Tkinter.Label(self.sw,text="'+S+'")')
			exec('self.sw.'+V+'lab.grid(row='+str(i)+',column=0,sticky="NSEW")')
			i=i+1
		self.sw.SnE = Tkinter.Button(self.sw,text="Save settings and exit",command=self.saveSets)
		self.sw.SnE.grid(row=3,column=0,columnspan=2,sticky="NSEW")
		self.sw.update()
		self.sw.geometry(self.sw.geometry())
		
	def saveSets(self):
		with open(self.HOME+"/.PythonJeopardy/DefaultSettings.cfg","w") as f:
			f.write("["+str(self.NP)+","+str(self.PC)+","+str(self.CC)+"]")
		self.clockDecision()
		self.playerDecision()
		self.pointDecision()
		self.sw.destroy()
	
	def playerDecision(self):
		try:
			for team in ["red","blue","green"]:
				exec('self.ScoreTime.'+team+'Frame.destroy()')
			self.ScoreTime.grid_columnconfigure(3,weight=0)
		except:
			iTried=0
		if self.NP:
			self.ScoreTime.Clock.grid(column=1,row=0,sticky='NSEW')
			self.ScoreTime.Teams = ["red","blue"]
			self.ScoreTime.TeamsSpot = [0,2]
		else:
			self.ScoreTime.grid_columnconfigure(3,weight=1)
			self.ScoreTime.Clock.grid(column=0,row=0,sticky='NSEW')
			self.ScoreTime.Teams = ["red","blue","green"]
			self.ScoreTime.TeamsSpot = [1,2,3]
		
	def pointDecision(self):
		self.ScoreTime.grid_columnconfigure(0,weight=1)
		self.ScoreTime.grid_rowconfigure(0,weight=1)
		for i,team in enumerate(self.ScoreTime.Teams):
			exec('self.ScoreTime.'+team+'Frame=Tkinter.Frame(self.ScoreTime)')
			exec('self.ScoreTime.grid_columnconfigure('+str(i+1)+',weight=1)')
			exec('self.ScoreTime.'+team+'Frame.'+team+'Score=Tkinter.IntVar()')
			exec('self.ScoreTime.'+team+'Frame.'+team+'lab=Tkinter.Label(self.ScoreTime.'+team+'Frame,bg="'+team+'",fg="white",textvariable=self.ScoreTime.'+team+'Frame.'+team+'Score,font=self.Font)')
			exec('self.ScoreTime.'+team+'Frame.'+team+'wager = Tkinter.IntVar()')
			exec('self.ScoreTime.'+team+'Frame.'+team+'Entry = Tkinter.Entry(self.ScoreTime.'+team+'Frame,textvariable=self.ScoreTime.'+team+'Frame.'+team+'wager,font=self.scoreFont,width=0)')
			if self.PC:
				if self.NP:
					if team=="blue":
						exec('self.ScoreTime.'+team+'Frame.'+team+'lab.grid(row=2,column=1,columnspan=3,sticky="NSEW")')
						exec('self.ScoreTime.'+team+'Frame.'+team+'Entry.grid(column=0,row=1,sticky="NSEW")')
					else:
						exec('self.ScoreTime.'+team+'Frame.'+team+'lab.grid(row=2,column=0,columnspan=3,sticky="NSEW")')
						exec('self.ScoreTime.'+team+'Frame.'+team+'Entry.grid(column=3,row=1,sticky="NSEW")')
				else:
					exec('self.ScoreTime.'+team+'Frame.'+team+'lab.grid(row=2,column=0,columnspan=3,sticky="NSEW")')
					exec('self.ScoreTime.'+team+'Frame.'+team+'Entry.grid(column=3,row=1,sticky="NSEW")')
				self.worth = [str(int(math.ceil(min(P)/2))),str(min(P)),str(max(P)),"wager"]
				#hehehe
				for row,operation,operand in [(0,"add","+"),(1,"sub","-")]:
					for col,worth in enumerate(self.worth):
						if worth != "wager":
							exec('def '+operation+str(col)+team+'():'+
								'\n    app.ScoreTime.'+team+'Frame.'+team+'Score.set(app.ScoreTime.'+team+'Frame.'+team+'Score.get()'+operand+'eval(app.worth['+str(col)+']))')
						else:
							exec('def '+operation+str(col)+team+'():'+
								'\n    app.ScoreTime.'+team+'Frame.'+team+'Score.set(app.ScoreTime.'+team+'Frame.'+team+'Score.get()'+operand+'app.ScoreTime.'+team+'Frame.'+team+'wager.get())')
						exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+' = Tkinter.Button(self.ScoreTime.'+team+'Frame,text="'+operand+worth+'",fg="white",bg="'+team+'",command='+operation+str(col)+team+',font=self.scoreFont)')
						if worth != "wager":
							if self.NP:
								if team == "blue":
									exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+'.grid(column='+str(col+1)+',row='+str(row)+',sticky="NSEW")')
								else:
									exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+'.grid(column='+str(col)+',row='+str(row)+',sticky="NSEW")')
							else:
								exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+'.grid(column='+str(col)+',row='+str(row)+',sticky="NSEW")')
						else:
							if self.NP:
								if team == "blue":
									exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+'.grid(column='+str(0)+',row='+str(row*2)+',sticky="NSEW")')
								else:
									exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+'.grid(column='+str(col)+',row='+str(row*2)+',sticky="NSEW")')
							else:
								exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+'.grid(column='+str(col)+',row='+str(row*2)+',sticky="NSEW")')
						exec('self.ScoreTime.'+team+'Frame.grid_columnconfigure('+str(col)+',weight=1)')
					exec('self.ScoreTime.'+team+'Frame.grid_rowconfigure('+str(row)+',weight=1)')
					exec('self.ScoreTime.'+team+'Frame.grid_rowconfigure(2,weight=1)')
			else:
				if self.NP:
					if team=="blue":
						exec('self.ScoreTime.'+team+'Frame.'+team+'lab.grid(row=1,column=1,sticky="NSEW")')
						exec('self.ScoreTime.'+team+'Frame.'+team+'Entry.grid(column=0,row=1,sticky="NSEW")')
					else:
						exec('self.ScoreTime.'+team+'Frame.'+team+'lab.grid(row=1,column=0,sticky="NSEW")')
						exec('self.ScoreTime.'+team+'Frame.'+team+'Entry.grid(column=1,row=1,sticky="NSEW")')
				else:
					exec('self.ScoreTime.'+team+'Frame.'+team+'lab.grid(row=1,column=0,sticky="NSEW")')
					exec('self.ScoreTime.'+team+'Frame.'+team+'Entry.grid(column=1,row=1,sticky="NSEW")')
				self.worth = ["","wager"]
				#hehehe
				for row,operation,operand in [(0,"add","+"),(2,"sub","-")]:
					for col,worth in enumerate(self.worth):
						if worth != "wager":
							exec('def '+operation+str(col)+team+'():'+
								'\n    app.ScoreTime.'+team+'Frame.'+team+'Score.set(app.ScoreTime.'+team+'Frame.'+team+'Score.get()'+operand+'eval(str(app.PTS)))')
						else:
							exec('def '+operation+str(col)+team+'():'+
								'\n    app.ScoreTime.'+team+'Frame.'+team+'Score.set(app.ScoreTime.'+team+'Frame.'+team+'Score.get()'+operand+'app.ScoreTime.'+team+'Frame.'+team+'wager.get())')
						exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+' = Tkinter.Button(self.ScoreTime.'+team+'Frame,text="'+operand+worth+'",fg="white",bg="'+team+'",command='+operation+str(col)+team+',font=self.scoreFont)')
						if self.NP:
							if team == "blue":
								newcol=[1,0]
								exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+'.grid(column='+str(newcol[col])+',row='+str(row)+',sticky="NSEW")')
							else:
								exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+'.grid(column='+str(col)+',row='+str(row)+',sticky="NSEW")')
						else:
							exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+'.grid(column='+str(col)+',row='+str(row)+',sticky="NSEW")')
						exec('self.ScoreTime.'+team+'Frame.grid_columnconfigure('+str(col)+',weight=1)')
					exec('self.ScoreTime.'+team+'Frame.grid_rowconfigure('+str(row)+',weight=1)')
			exec('self.ScoreTime.'+team+'Frame.grid(row=0,column='+str(self.ScoreTime.TeamsSpot[i])+',sticky="NSEW")')
	
	def iHateYouTkInter(self): #It won't update textvariables on the point buttons on the scoreboard.
		if self.Round <3:
			if self.PC:
				self.P=eval(str(self.clusterfuck[1]))
				self.worth = [str(int(math.ceil(min(P)/2))),str(min(P)),str(max(P)),"wager"]
				#hehehe
				for team in self.ScoreTime.Teams:
					for row,operation,operand in [(0,"add","+"),(1,"sub","-")]:
						for col,worth in enumerate(self.worth):
							exec('self.ScoreTime.'+team+'Frame.button_'+operation+str(col)+team+'.config(text="'+operand+worth+'")')
	
	def clockDecision(self):
		if self.CC:
			self.ScoreTime.Clock.timeEntry.grid(column=0,row=0,sticky='NSEW')
			self.ScoreTime.Clock.button_ST.grid(column=0,row=1,sticky='NSEW')
			self.ScoreTime.Clock.labelTime.grid(column=0,row=2,sticky='NSEW')
		else:
			self.ScoreTime.Clock.timeEntry.grid(column=0,row=0,sticky='NSEW')
			self.ScoreTime.Clock.labelTime.grid(column=0,row=1,rowspan=2,sticky='NSEW')
			
		
		
if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title('Python Jeopardy')
	app.mainloop()
	
