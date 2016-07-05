#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
"""
Goals:
+Long term: maybe make a speed round thing?
++Needs persistent point values
++One button to toggle "show"/"arcade" mode
"""

import Tkinter
import math
import os
import csv
import glob

class simpleapp_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
	
	def initialize(self):
		self.grid()
		
		if not os.path.exists(os.getcwd()+'/.PythonFeud'):
			os.mkdir(os.getcwd()+'/.PythonFeud')
		self.HOME = os.getcwd()
		
		###########################################
		#SOME VARIABLES
		###########################################
		self.FontSize = Tkinter.IntVar()
		self.FontSize.set(10)	
		
		
		###########################################
		#ROW0
		###########################################
		
		self.roundTitle = Tkinter.StringVar()
		self.roundTitle.set("Type the question here")
		self.enterTitle = Tkinter.Entry(self,textvariable=self.roundTitle)
		self.enterTitle.grid(column=0,columnspan=2,row=0,sticky="NSEW")
		
		self.instlabel = Tkinter.Label(self,text='filename:')
		self.instlabel.grid(column=2,row=0,sticky='NSEW')
		
		self.saveload = Tkinter.StringVar()
		self.nameEntry = Tkinter.Entry(self,textvariable=self.saveload,width=10)
		self.nameEntry.grid(column=3,row=0,sticky='NSEW')
		
		self.OPbutt = Tkinter.Menubutton(self,text=u"Open file",relief="raised")
		self.OpenMenu = Tkinter.Menu(self.OPbutt,tearoff=0)
		self.OPbutt["menu"] = self.OpenMenu
		for i,name in enumerate(glob.glob(self.HOME+'/.PythonFeud/*.csv')):
			if name:
				exec('def Open'+str(i)+'():'+
					'\n    app.shortenit = "'+name+'"'+
					'\n    app.shortenit = app.shortenit.replace(app.HOME+"/.PythonFeud/","")'+
					'\n    app.shortenit = app.shortenit.replace(".csv","")'+
					'\n    app.saveload.set(app.shortenit)'+
					'\n    app.loadit()')
				exec('self.OpenMenu.add_command(label="'+name+'", command=Open'+str(i)+')')
			else:
				self.OpenMenu.add_command(label="{None Found}")
		self.OPbutt.grid(column=4,row=0,sticky='NSWE')
		
		self.SAVbutt = Tkinter.Button(self,text=u"Save file",command=self.confirmit,relief="raised")
		self.SAVbutt.grid(column=5,row=0,sticky='NSWE')
		
		self.FontAdj = Tkinter.Button(self,text=u"Auto-adjust font",command=self.fontAdj)
		self.FontAdj.grid(column=6,row=0,sticky='NSWE')

		###########################################
		#ROW1
		###########################################

		self.anslablabel1 = Tkinter.Label(self,text='Answers')
		self.anslablabel1.grid(column=0,row=1,sticky='NSEW')
		self.anslablabel2 = Tkinter.Label(self,text='Answers')
		self.anslablabel2.grid(column=5,row=1,sticky='NSEW')
		
		self.poilablabel1 = Tkinter.Label(self,text='Points')
		self.poilablabel1.grid(column=1,row=1,sticky='NSEW')
		self.poilablabel2 = Tkinter.Label(self,text='Points')
		self.poilablabel2.grid(column=6,row=1,sticky='NSEW')

		###########################################
		#Arraymaker
		###########################################

		for i in range(0,8):
			exec('def show'+str(i)+'():'+
				'\n    if app.potadd'+str(i)+'.config("relief")[-1] != "sunken":'+
				'\n        app.potadd'+str(i)+'.config(relief="sunken")'+
				'\n        app.Pot.set(app.Pot.get()+app.point'+str(i)+'.get())'+
				'\n        app.ShowWindow.BoxLabel'+str(i)+'.set(app.answer'+str(i)+'.get())'+
				'\n        ws=app.ShowWindow.winfo_width()'+
				'\n        Wrap=int(math.ceil(ws/8*3))'+
				'\n        app.ShowWindow.Box'+str(i)+'.config(fg="black",bg="white",wraplength=Wrap)'+
				'\n        app.ShowWindow.BoxPnt'+str(i)+'.config(bg="gray",textvariable=app.point'+str(i)+')')
			exec('self.answer'+str(i)+' = Tkinter.StringVar()')
			exec('self.answer'+str(i)+'.set("Answer #'+str(i+1)+'")')
			exec('self.answerbox'+str(i)+' = Tkinter.Entry(self,textvariable=self.answer'+str(i)+')')
			exec('self.point'+str(i)+' = Tkinter.IntVar()')
			exec('self.pointbox'+str(i)+' = Tkinter.Entry(self,textvariable=self.point'+str(i)+',width=5)')
			exec('self.potadd'+str(i)+' = Tkinter.Button(self,text=u"Show",command=show'+str(i)+')')
			if i<4:
				exec('self.answerbox'+str(i)+'.grid(column=0,row='+str(i+1)+',sticky="NSEW")')
				exec('self.pointbox'+str(i)+'.grid(column=1,row='+str(i+1)+',sticky="NSEW")')
				exec('self.potadd'+str(i)+'.grid(column=2,row='+str(i+1)+',sticky="NSEW")')
			else:
				exec('self.answerbox'+str(i)+'.grid(column=4,row='+str(i-3)+',sticky="NSEW")')
				exec('self.pointbox'+str(i)+'.grid(column=5,row='+str(i-3)+',sticky="NSEW")')
				exec('self.potadd'+str(i)+'.grid(column=6,row='+str(i-3)+',sticky="NSEW")')
		
		###########################################
		#COLUMN3
		###########################################
		
		self.Pot = Tkinter.IntVar()
		self.Pot.set(0)
		self.PotBox = Tkinter.Label(self,textvariable=self.Pot)
		self.PotBox.grid(column=3,row=1,rowspan=2,sticky="NSEW")
		self.BoardMaker = Tkinter.Button(self,text=u"Create a new board",command=self.MakeBoard)
		self.BoardMaker.grid(column=3,row=3,rowspan=2,sticky="NSEW")

		###########################################
		#ROW5
		###########################################
		
		for x,team in enumerate(["Red","Blue"]):
			exec('self.'+team+'Score = Tkinter.IntVar()')
			exec('self.'+team+'Score.set(0)')
			exec('self.'+team+'Pts = Tkinter.Button(self,bg="'+team+'",fg="white",text=u"Add pot",command=self.'+team+'AddPts)')
			exec('self.'+team+'Pts.grid(column='+str(x*4)+',row=5,columnspan=3,sticky="NSEW")')

		###########################################
		#ROW6
		###########################################
		
		for x,team in enumerate(["Red","Blue"]):
			exec('self.Man'+team+' = Tkinter.IntVar()')
			exec('self.Man'+team+'Box = Tkinter.Entry(self,textvariable=self.Man'+team+')')
			exec('self.Man'+team+'Box.grid(column='+str(x*4)+',row=6,sticky="NSEW")')
			exec('self.'+team+'UpButt = Tkinter.Button(self,fg="white",bg="'+team+'",text=u"Update score",command=self.Update'+team+')')
			exec('self.'+team+'UpButt.grid(column='+str(x*4+1)+',row=6,columnspan=2,sticky="NSEW")')

		###########################################
		#ROW7
		###########################################
		
		for i,team in enumerate(["Red","Blue"]):
			exec('self.'+team+'Strike = Tkinter.IntVar()')
			exec('self.'+team+'Strike.set(0)')
			exec('self.'+team+'StrikeCounter = Tkinter.Button(self,bg="'+team+'",fg="white",text=u"Add strike",command=self.'+team+'StrikeAdd)')
			exec('self.'+team+'StrikeCounter.grid(column='+str(i*4)+',columnspan=3,row=7,sticky="NSEW")')
		
		###########################################
		#Geometry stuff
		###########################################
		
		self.resizable(True,True)
		self.update()
		self.geometry(self.geometry())
		
	###########################################
	#My Definitions
	###########################################
	
	def LaunchConfig(self):
		if self.conf.config('relief')[-1] == 'sunken':
			self.ConfWindow.destroy()
			self.conf.config(relief="raised",text=u"Settings")
		else:
			self.conf.config(relief="sunken",text=u"Settings")
			self.ConfWindow = Tkinter.Toplevel(self)
			self.ConfWindow.wm_grid()
			self.ConfWindow.wm_title("Settings")
			self.ConfWindow.FontUp = Tkinter.Button(self.ConfWindow,text=u"+",command=self.fontUp)
			self.ConfWindow.FontUp.grid(column=0,row=0,sticky="NSEW")
			self.ConfWindow.FontDown = Tkinter.Button(self.ConfWindow,text=u"-",command=self.fontDown)
			self.ConfWindow.FontDown.grid(column=0,row=2,sticky="NSEW")
			self.ConfWindow.FontLab = Tkinter.Label(self.ConfWindow,textvariable=self.FontSize)
			self.ConfWindow.FontLab.grid(column=0,row=1)
			self.ConfSave = Tkinter.Button(self.ConfWindow,text=u"save",command=self.saveConf)
			self.ConfSave.grid(column=1,row=1,sticky="NSEW")
	
	def fontAdj(self):
		ws = self.ShowWindow.winfo_width()
		self.FontSize.set(int(math.ceil(ws/54)))
		self.ShowWindow.RedScore.config(font=("system",self.FontSize.get()))
		self.ShowWindow.Potbox.config(font=("system",self.FontSize.get()))
		self.ShowWindow.BlueScore.config(font=("system",self.FontSize.get()))
		self.ShowWindow.Title.config(font=("system",self.FontSize.get()))
		for x,team in enumerate(["Red","Blue"]):
			for i in range(1,4):
				exec('self.ShowWindow.'+team+'StrikeCounter'+str(i)+'.config(font=("system",self.FontSize.get()))')
		for i in range(0,8):
			try:
				exec('self.ShowWindow.Box'+str(i)+'.config(font=("system",self.FontSize.get()))')
				exec('self.ShowWindow.BoxPnt'+str(i)+'.config(font=("system",self.FontSize.get()))')
				exec('self.ShowWindow.Box'+str(i)+'.config(font=("system",self.FontSize.get()))')
			except:
				oops = 0
	
	def loadit(self):
		data = {}
		Y=0
		# here the magic begins (a.k.a. not my code)
		# open file and create reader
		with open(self.HOME + "/.PythonFeud/%s.csv" % self.saveload.get(), 'rb') as f:
			reader = csv.reader(f)
			# read header
			header = reader.next()
			# create list for each column
			for name in header:
				data[name] = []
			# read rows, append values to lists
			for row in reader:
				for i, value in enumerate(row):
					data[header[i]].append(value)
		self.roundTitle.set(data[header[1]][0])
		for i in range(1,9):
			exec('self.answer'+str(i-1)+'.set(data[header[0]][i])')
			exec('self.point'+str(i-1)+'.set(data[header[1]][i])')
	
	def confirmit(self):
		self.t = Tkinter.Toplevel(self)
		self.t.wm_title("Are you sure")
		self.t.y = Tkinter.Button(self.t, text=u"Click to confirm save",command=self.saveit)
		self.t.y.grid(column=0,sticky='NSEW')
	
	def saveit(self):
		os.system("rm "+self.HOME +"/.PythonFeud/%s.csv" % self.saveload.get())
		f = open(self.HOME + "/.PythonFeud/%s.csv" % self.saveload.get(), 'a')
		f.write('"Answer","Points"\n"Round Name","'+self.roundName.get()+'"\n')
		for i in range(0,8):
			exec('ANS=self.answer'+str(i)+'.get()')
			exec('PNT=self.point'+str(i)+'.get()')
			f.write('"%s","%s"\n' % (ANS,PNT))
		f.close()
		self.t.destroy()
	
	def UpdateRed(self):
		self.RedScore.set(self.ManRed.get())
		
	def UpdateBlue(self):
		self.BlueScore.set(self.ManBlue.get())
		
	def RedAddPts(self):
		if self.BoardMaker.config('relief')[-1] == "sunken":
			self.RedScore.set(self.RedScore.get()+self.Pot.get())
			self.Pot.set(0)

	def BlueAddPts(self):
		if self.BoardMaker.config('relief')[-1] == "sunken":
			self.BlueScore.set(self.BlueScore.get()+self.Pot.get())
			self.Pot.set(0)
	
	for team in ["Red","Blue"]:	
		exec('def '+team+'StrikeAdd(self):'+
			'\n    if app.BoardMaker.config("relief")[-1] == "sunken":'+
			'\n        app.'+team+'Strike.set(app.'+team+'Strike.get()+1)'+
			'\n        if app.'+team+'Strike.get()<4:'+
			'\n            circumvent = str("app.ShowWindow.'+team+'StrikeCounter"+str(app.'+team+'Strike.get()))'+
			'\n            eval(circumvent+".config(text=\'X\')")')

	####################################################################

	def MakeBoard(self):
		if self.BoardMaker.config('relief')[-1] == 'sunken':
			self.Pot.set(0)
			for team in ["Red","Blue"]:
				exec('self.'+team+'Score.set(0)')
				exec('self.'+team+'Strike.set(0)')
			for i in range(0,8):
				exec('self.potadd'+str(i)+'.config(relief="raised")')
			self.ShowWindow.destroy()
			self.BoardMaker.config(relief="raised",text=u"Create a new board")
		else:
			self.BoardMaker.config(relief="sunken",text=u"Close board")
			self.ShowWindow = Tkinter.Toplevel(self)
			self.ShowWindow.wm_grid()
			self.ShowWindow.wm_title("Python Feud!")
			counter = 0
			#ROW0
			for x,team in enumerate(["Red","Blue"]):
				exec('self.ShowWindow.'+team+'Score = Tkinter.Label(self.ShowWindow,fg="white",bg="'+team+'",textvariable=self.'+team+'Score,font=("system",self.FontSize.get()))')
				exec('self.ShowWindow.'+team+'Score.grid(column='+str(x*5)+',columnspan=3,row=0,sticky="NSEW")')
			self.ShowWindow.Potbox = Tkinter.Label(self.ShowWindow,fg="white",bg="black",textvariable=self.Pot,font=("system",self.FontSize.get()))
			self.ShowWindow.Potbox.grid(column=3,columnspan=2,row=0,rowspan=2,sticky="NSEW")
			#ROW1
			for x,team in enumerate(["Red","Blue"]):
				for i in range(0,3):
					exec('self.ShowWindow.'+team+'StrikeCounter'+str(i+1)+' = Tkinter.Label(self.ShowWindow,bg="'+team+'",fg="white",font=("system",self.FontSize.get()))')
					exec('self.ShowWindow.'+team+'StrikeCounter'+str(i+1)+'.grid(column='+str(x*5+i)+',row=1,sticky="NSEW")')
			#ROW2
			self.ShowWindow.Title = Tkinter.Label(self.ShowWindow,textvariable=self.roundTitle,fg="white",bg="black",font=("system",self.FontSize.get()))
			self.ShowWindow.Title.grid(column=0,columnspan=8,row=2,sticky="NSEW")
			#ARRAYMAKER
			for i in range(0,8):
				checker = eval('app.answer'+str(i)+'.get()')
				if checker:
					counter = counter +1
					exec('self.ShowWindow.BoxLabel'+str(i)+' = Tkinter.StringVar()')
					exec('self.ShowWindow.BoxLabel'+str(i)+'.set(counter)')
					if i<4:
						exec('self.ShowWindow.Box'+str(i)+' = Tkinter.Label(self.ShowWindow,fg="white",bg="black",textvariable=self.ShowWindow.BoxLabel'+str(i)+',font=("system",self.FontSize.get()))')
						exec('self.ShowWindow.Box'+str(i)+'.grid(column=0,columnspan=3,row='+str(i+3)+',sticky="NSEW")')
						exec('self.ShowWindow.BoxPnt'+str(i)+' = Tkinter.Label(self.ShowWindow,fg="white",bg="black",font=("system",self.FontSize.get()))')
						exec('self.ShowWindow.BoxPnt'+str(i)+'.grid(column=3,row='+str(i+3)+',sticky="NSEW")')
					else:
						exec('self.ShowWindow.Box'+str(i)+' = Tkinter.Label(self.ShowWindow,fg="white",bg="black",textvariable=self.ShowWindow.BoxLabel'+str(i)+',font=("system",self.FontSize.get()))')
						exec('self.ShowWindow.Box'+str(i)+'.grid(column=4,columnspan=3,row='+str(i-1)+',sticky="NSEW")')
						exec('self.ShowWindow.BoxPnt'+str(i)+' = Tkinter.Label(self.ShowWindow,fg="white",bg="black",font=("system",self.FontSize.get()))')
						exec('self.ShowWindow.BoxPnt'+str(i)+'.grid(column=7,row='+str(i-1)+',sticky="NSEW")')
			#GEOMETRY
			for i in range(0,8):
				exec('self.ShowWindow.grid_columnconfigure('+str(i)+',weight=1)')
			for i in range(0,int(math.ceil(counter/2)+3)):
				if i < 3:
					exec('self.ShowWindow.grid_rowconfigure(0,weight=1)')
				else:
					exec('self.ShowWindow.grid_rowconfigure('+str(i)+',weight=2)')
			
			self.ShowWindow.resizable(True,True)
			self.ShowWindow.update()
			self.ShowWindow.geometry(self.ShowWindow.geometry())


if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title('PythonFeud Control Center')
	app.mainloop()
