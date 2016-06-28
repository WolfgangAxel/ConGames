#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
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
		if not os.path.exists(os.getcwd()+'/.PythonJeopardy'):
			os.mkdir(os.getcwd()+'/.PythonJeopardy')
		
		self.menya = Tkinter.Menu(self)
		self.OpenMenu = Tkinter.Menu(self.menya,tearoff=0)
		for i,name in enumerate(glob.glob(os.getcwd()+'/.PythonJeopardy/*.board')):
			if name:
				exec('def Open'+str(i)+'():'+
					'\n    app.OpenFile ="'+name+'"'+
					'\n    app.arrayload()')
				exec('self.OpenMenu.add_command(label="'+name+'", command=Open'+str(i)+')')
			else:
				self.OpenMenu.add_command(label="{None Found}")
		self.menya.add_cascade(label="Open",menu=self.OpenMenu)
		self.menya.add_command(label="Auto Font Size",command=self.fontadj)
		self.menya.add_command(label="Quit",command=self.die)
		self.config(menu=self.menya)
		
		################################################################
		#						   Game Board						   #
		################################################################
		self.gb = Tkinter.Frame(self)
		self.gb.grid(column=0,row=0,sticky="NSEW")
		
		self.FontSize = Tkinter.IntVar()
		self.FontSize.set(int(math.ceil(self.winfo_width()/68)))
		
		for i,worth in enumerate(["1","2","3","4","5"]):
			for j,cat in enumerate(["a","b","c","d","e"]):
				exec('self.gb.catlab'+str(j)+' = Tkinter.Label(self.gb,text="'+cat+'",wraplength=100,font=("Sans Serif",self.FontSize.get()),width='+str(self.winfo_width()/5)+',relief="raised",bg="white")')
				exec('self.gb.catlab'+str(j)+'.grid(column='+str(j)+',row=0,sticky="NSEW")')
				exec('self.gb.box'+str(j)+'x'+str(i+1)+' = Tkinter.Button(self.gb,text="'+worth+'",command=self.reveal'+str(j)+'x'+str(i+1)+',font=("Sans Serif",self.FontSize.get()),width='+str(self.winfo_width()/5)+')')
				exec('self.gb.box'+str(j)+'x'+str(i+1)+'.grid(column='+str(j)+',row='+str(i+1)+',sticky="NSEW")')
		
		for i in range(0,6):
			if i<5:
				exec('self.gb.grid_columnconfigure('+str(i)+',weight=1)')
			exec('self.gb.grid_rowconfigure('+str(i)+',weight=1)')
		
		################################################################
		#						   Score&Time						   #
		################################################################
		
		self.ScoreTime = Tkinter.Frame(self)
		self.ScoreTime.grid(column=0,row=1,sticky="NSEW")
		
		self.ScoreTime.timeOut = Tkinter.StringVar()
		self.ScoreTime.timeOut.set("Time's up!")
		
		self.ScoreTime.timeValue = Tkinter.IntVar()
		self.ScoreTime.entry = Tkinter.Entry(self.ScoreTime,textvariable=self.ScoreTime.timeValue)
		self.ScoreTime.entry.grid(column=4,row=0,sticky='NSEW')
		self.ScoreTime.timeValue.set(20)
		
		self.ScoreTime.redwager = Tkinter.IntVar()
		self.ScoreTime.entry = Tkinter.Entry(self.ScoreTime,textvariable=self.ScoreTime.redwager)
		self.ScoreTime.entry.grid(column=3,row=1,sticky='NSEW')
		
		self.ScoreTime.bluewager = Tkinter.IntVar()
		self.ScoreTime.entry = Tkinter.Entry(self.ScoreTime,textvariable=self.ScoreTime.bluewager)
		self.ScoreTime.entry.grid(column=5,row=1,sticky='NSEW')
		
		rowcount=0
		for operation in ["add","sub"]:
			if operation == "add":
				operand = '+'
			else:
				operand = '-'
			columncount=0
			for worth in ["50","100","500","wager"]:
				teamcount=0
				for team in ["red","blue"]:
					exec('self.ScoreTime.button_'+operation+worth+team+' = Tkinter.Button(self.ScoreTime,text=u"'+operand+worth+'",fg="white",bg="'+team+'",command=self.'+operation+worth+team+')')
					columnfinal=teamcount+columncount
					if worth != "wager":
						exec('self.ScoreTime.button_'+operation+worth+team+'.grid(column='+str(columnfinal)+',row='+str(rowcount)+',sticky="NSEW")')
						teamcount=6
					else:
						exec('self.ScoreTime.button_'+operation+worth+team+'.grid(column='+str(columnfinal)+',row='+str(rowcount*2)+',sticky="NSEW")')
						teamcount=2
				columncount=columncount+1
			rowcount=rowcount+1
		
		self.ScoreTime.redScore = Tkinter.IntVar()
		self.ScoreTime.labelRed = Tkinter.Label(self.ScoreTime,textvariable=self.ScoreTime.redScore,fg="white",bg="red",font=("DwarfFortressVan", 25))
		self.ScoreTime.labelRed.grid(column=0,row=2,columnspan=3,sticky='NSEW')
		self.ScoreTime.redScore.set(0)
		
		self.ScoreTime.blueScore = Tkinter.IntVar()
		self.ScoreTime.labelBlue = Tkinter.Label(self.ScoreTime,textvariable=self.ScoreTime.blueScore,fg="white",bg="blue",font=("DwarfFortressVan", 25))
		self.ScoreTime.labelBlue.grid(column=6,row=2,columnspan=3,sticky='NSEW')
		self.ScoreTime.blueScore.set(0)
		
		self.ScoreTime.button_ST = Tkinter.Button(self.ScoreTime, text=u"Start Clock",command=self.startClock, relief="raised")
		self.ScoreTime.button_ST.grid(column=4,row=1,sticky='NSEW')
		
		self.ScoreTime.timeCountdown = Tkinter.IntVar()
		self.ScoreTime.labelTime = Tkinter.Label(self.ScoreTime,textvariable=self.ScoreTime.timeCountdown,font=("DwarfFortressVan", 25))
		self.ScoreTime.labelTime.grid(column=4,row=2,sticky='NSEW')
		self.ScoreTime.timeCountdown.set(self.ScoreTime.timeValue.get())
		
		self.ScoreTime.timerStart = Tkinter.BooleanVar()
		self.ScoreTime.timerStart.set(False)
		
		for i in range(0,9):
			exec('self.ScoreTime.grid_columnconfigure('+str(i)+',weight=1)')
			exec('self.ScoreTime.grid_rowconfigure('+str(i)+',weight=1)')
		self.grid_rowconfigure(0,weight=5)
		self.grid_rowconfigure(1,weight=0)
		self.grid_columnconfigure(0,weight=1)
		self.resizable(True,True)
		self.update()
		self.geometry(self.geometry())
		self.grid()
	
	####################################################################
	#							  Definitions						   #
	####################################################################
	
	def arrayload(self):
		f=open(self.OpenFile,'r')
		self.clusterfuck = {}
		self.clusterfuck = eval(str(f.read()))
		for cat in range(0,5):
			exec('self.gb.catlab'+str(cat)+'.config(text="'+str(eval(str(eval(str(self.clusterfuck[0]))[cat]))[0])+'")')
			for ques in range(1,6):
				exec('self.gb.box'+str(cat)+'x'+str(ques)+'.config(text=str(eval(str(self.clusterfuck[1]))['+str(ques-1)+']),state="normal")')
		f.close()
		
	def startClock(self):
		if self.ScoreTime.button_ST.config('relief')[-1] == "sunken":
			self.ScoreTime.button_ST.config(relief="raised")
			self.ScoreTime.button_ST.config(text="Start Clock")
			self.ScoreTime.timerStart.set(False)
			self.ScoreTime.timeCountdown.set(self.ScoreTime.timeValue.get())
			self.ScoreTime.labelTime.config(textvariable=self.ScoreTime.timeCountdown)
		else:
			self.ScoreTime.button_ST.config(relief="sunken")
			self.ScoreTime.button_ST.config(text="Reset Clock")
			self.ScoreTime.timeCountdown.set(self.ScoreTime.timeValue.get())
			self.ScoreTime.timerStart.set(True)
			self.countdown()
	
	def countdown(self):
		if self.ScoreTime.timerStart.get():
			if self.ScoreTime.timeCountdown.get()>0:
				self.ScoreTime.timeCountdown.set(self.ScoreTime.timeCountdown.get()-1)
				self.ScoreTime.after(1000,self.countdown)
			else:
				self.ScoreTime.labelTime.config(textvariable=self.ScoreTime.timeOut)
				self.ScoreTime.timerStart.set(False)
	
	def die(self):
		self.destroy()
		
	for operation in ["add","sub"]:
		if operation == "add":
			operand = '+'
		else:
			operand = '-'
		for worth in ["50","100","500","wager"]:
			for team in ["red","blue"]:
				if worth != "wager":
					exec('def '+operation+worth+team+'(self):'+
						'\n    self.ScoreTime.'+team+'Score.set(self.ScoreTime.'+team+'Score.get()'+operand+worth+')')
				else:
					exec('def '+operation+worth+team+'(self):'+
						'\n    self.ScoreTime.'+team+'Score.set(self.ScoreTime.'+team+'Score.get()'+operand+'self.ScoreTime.'+team+worth+'.get())')
	
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
		self.qna.pointlabel=Tkinter.Label(self.qna,text=self.PTS,font=("Sans Serif",self.FontSize.get()))
		self.qna.pointlabel.grid(row=0,sticky="NSEW")
		if eval('str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))[self.CAT]))[1]))[self.QUES-1]))[2])'):
			self.qna.path=Image.open(str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))[self.CAT]))[1]))[self.QUES-1]))[2]))
			imgwidth, imgheight=self.qna.path.size
			for dim in ["width","height"]:
				scaleheight=self.gb.winfo_height()/10*7
				scalewidth=self.gb.winfo_width()-int(self.FontSize.get())
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
				self.qna.question=Tkinter.Label(self.qna,text=str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))[self.CAT]))[1]))[self.QUES-1]))[0]),wraplength=self.winfo_width()-int(self.FontSize.get()),font=("Sans Serif",self.FontSize.get()))
				self.qna.question.grid(row=2,sticky="NSEW")
			else:
				totrow=3
		else:
			totrow=3
			self.qna.question=Tkinter.Label(self.qna,text=str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))[self.CAT]))[1]))[self.QUES-1]))[0]),wraplength=self.winfo_width()-int(self.FontSize.get()),font=("Sans Serif",self.FontSize.get()))
			self.qna.question.grid(row=1,sticky="NSEW")
		self.qna.flip=Tkinter.Button(self.qna,text="Reveal",command=self.showans,font=("Sans Serif",self.FontSize.get()))
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
	
	def showans(self):
		self.qna.grid_remove()
		self.ans = Tkinter.Frame(self)
		self.ans.pointlabel=Tkinter.Label(self.ans,text=self.PTS,font=("Sans Serif",self.FontSize.get()))
		self.ans.pointlabel.grid(row=0,sticky="NSEW")
		self.ans.answer=Tkinter.Label(self.ans,text=str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))[self.CAT]))[1]))[self.QUES-1]))[1]),wraplength=self.winfo_width()-int(self.FontSize.get()),font=("Sans Serif",self.FontSize.get()))
		self.ans.answer.grid(row=1,sticky="NSEW")
		self.ans.returnbtn=Tkinter.Button(self.ans,text="Return to Board",command=self.returntoboard,font=("Sans Serif",self.FontSize.get()))
		self.ans.returnbtn.grid(row=2,sticky="NSEW")
		self.ans.columnconfigure(0,weight=1)
		self.ans.rowconfigure(0,weight=0)
		self.ans.rowconfigure(1,weight=1)
		self.ans.rowconfigure(2,weight=0)
		self.ans.grid(column=0,row=0,sticky="NSEW")
		
	def returntoboard(self):
		self.ans.grid_remove()
		self.gb.grid(column=0,row=0,sticky="NSEW")

	def fontadj(self):
		ws=self.winfo_width()
		self.FontSize=Tkinter.StringVar()
		self.FontSize.set(int(math.ceil(ws/68)))
		for cat in range(0,5):
			for ques in range(1,6):
				exec('self.gb.catlab'+str(cat)+'.config(font=("Sans Serif",self.FontSize.get()),wraplength='+str(int(math.ceil(ws/5)))+')')
				exec('self.gb.box'+str(cat)+'x'+str(ques)+'.config(font=("Sans Serif",self.FontSize.get()),wraplength='+str(int(math.ceil(ws/5)))+')')
		
if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title('Python Jeopardy')
	app.mainloop()
