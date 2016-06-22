#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
import math
import os
import csv

class simpleapp_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
	
	def initialize(self):
		self.grid()
		
		###########################################
		#ROW0
		###########################################
		
		self.inst = Tkinter.StringVar()
		self.inst.set('Filename:')
		self.instlabel = Tkinter.Label(self,textvariable=self.inst)
		self.instlabel.grid(column=2,row=0,sticky='NSEW')
		
		self.saveload = Tkinter.StringVar()
		self.nameEntry = Tkinter.Entry(self,textvariable=self.saveload,width=10)
		self.nameEntry.grid(column=3,row=0,sticky='NSEW')
		
		self.OPbutt = Tkinter.Button(self,text=u"Open file",command=self.loadit,relief="raised")
		self.OPbutt.grid(column=4,row=0,sticky='NSWE')
		
		self.SAVbutt = Tkinter.Button(self,text=u"Save file",command=self.confirmit,relief="raised")
		self.SAVbutt.grid(column=5,row=0,sticky='NSWE')

		###########################################
		#ROW1
		###########################################

		self.anslab = Tkinter.StringVar()
		self.anslab.set('Answers')
		self.anslablabel1 = Tkinter.Label(self,textvariable=self.anslab)
		self.anslablabel1.grid(column=0,row=1,sticky='NSEW')
		self.anslablabel2 = Tkinter.Label(self,textvariable=self.anslab)
		self.anslablabel2.grid(column=5,row=1,sticky='NSEW')
		
		self.poilab = Tkinter.StringVar()
		self.poilab.set('points')
		self.poilablabel1 = Tkinter.Label(self,textvariable=self.poilab)
		self.poilablabel1.grid(column=1,row=1,sticky='NSEW')
		self.poilablabel2 = Tkinter.Label(self,textvariable=self.poilab)
		self.poilablabel2.grid(column=6,row=1,sticky='NSEW')

		###########################################
		#Arraymaker
		###########################################

		for i in range(0,8):
			exec('def show'+str(i)+'():'+
				'\n        app.Pot.set(app.Pot.get()+app.point'+str(i)+'.get())'+
				'\n        app.ShowWindow.BoxLabel'+str(i)+'.set(app.answer'+str(i)+'.get())'+
				'\n        app.ShowWindow.Box'+str(i)+'.config(fg="black",bg="white")'+
				'\n        app.ShowWindow.BoxPnt'+str(i)+'.config(bg="gray",textvariable=app.point'+str(i)+')')
			if i<4:
				exec('self.answer'+str(i)+' = Tkinter.StringVar()')
				exec('self.answerbox'+str(i)+' = Tkinter.Entry(self,textvariable=self.answer'+str(i)+')')
				exec('self.answerbox'+str(i)+'.grid(column=0,row='+str(i+1)+',sticky="NSEW")')
				exec('self.point'+str(i)+' = Tkinter.IntVar()')
				exec('self.pointbox'+str(i)+' = Tkinter.Entry(self,textvariable=self.point'+str(i)+',width=5)')
				exec('self.pointbox'+str(i)+'.grid(column=1,row='+str(i+1)+',sticky="NSEW")')
				exec('self.potadd'+str(i)+' = Tkinter.Button(self,text=u"Show",command=show'+str(i)+')')
				exec('self.potadd'+str(i)+'.grid(column=2,row='+str(i+1)+',sticky="NSEW")')
			else:
				exec('self.answer'+str(i)+' = Tkinter.StringVar()')
				exec('self.answerbox'+str(i)+' = Tkinter.Entry(self,textvariable=self.answer'+str(i)+')')
				exec('self.answerbox'+str(i)+'.grid(column=4,row='+str(i-3)+',sticky="NSEW")')
				exec('self.point'+str(i)+' = Tkinter.IntVar()')
				exec('self.pointbox'+str(i)+' = Tkinter.Entry(self,textvariable=self.point'+str(i)+',width=5)')
				exec('self.pointbox'+str(i)+'.grid(column=5,row='+str(i-3)+',sticky="NSEW")')
				exec('self.potadd'+str(i)+' = Tkinter.Button(self,text=u"Add",command=show'+str(i)+')')
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
		
		self.RedScore = Tkinter.IntVar()
		self.RedScore.set(0)
		self.RedPts = Tkinter.Button(self,bg="red",fg="white",text=u"Add pot",command=self.RedAddPts)
		self.RedPts.grid(column=0,row=5,columnspan=3,sticky='NSEW')
		
		self.BlueScore = Tkinter.IntVar()
		self.BlueScore.set(0)
		self.BluePts = Tkinter.Button(self,bg="blue",fg="white",text=u"Add pot",command=self.BlueAddPts)
		self.BluePts.grid(column=4,row=5,columnspan=3,sticky='NSEW')

		###########################################
		#ROW6
		###########################################
		
		self.ManRed = Tkinter.IntVar()
		self.ManRedBox = Tkinter.Entry(self,textvariable=self.ManRed)
		self.ManRedBox.grid(column=0,row=6,sticky='NSEW')
		self.RedUpButt = Tkinter.Button(self,fg="white",bg="red",text=u"Update score",command=self.UpdateRed)
		self.RedUpButt.grid(column=1,row=6,columnspan=2,sticky='NSEW')
		
		self.ManBlue = Tkinter.IntVar()
		self.ManBlueBox = Tkinter.Entry(self,textvariable=self.ManBlue,width=10)
		self.ManBlueBox.grid(column=4,row=6,sticky='NSEW')
		self.BlueUpButt = Tkinter.Button(self,fg="white",bg="blue",text=u"Update score",command=self.UpdateBlue)
		self.BlueUpButt.grid(column=5,row=6,columnspan=2,sticky='NSEW')

		###########################################
		#ROW7
		###########################################
		
		self.RedStrike = Tkinter.StringVar()
		self.RedStrike.set('')
		self.RedStrikeCounter = Tkinter.Button(self,bg="red",fg="white",text=u"Add strike",command=self.RedStrikeAdd)
		self.RedStrikeCounter.grid(column=0,columnspan=3,row=7,sticky="NSEW")
		self.BlueStrike = Tkinter.StringVar()
		self.BlueStrike.set('')
		self.BlueStrikeCounter = Tkinter.Button(self,bg="blue",fg="white",text=u"Add strike",command=self.BlueStrikeAdd)
		self.BlueStrikeCounter.grid(column=4,columnspan=3,row=7,sticky="NSEW")
		
		###########################################
		#Geometry stuff
		###########################################
		
		self.resizable(True,True)
		self.update()
		self.geometry(self.geometry())
		
	###########################################
	#My Definitions
	###########################################
	def loadit(self):
		data = {}
		Y=0
		# here the magic begins (a.k.a. not my code)
		# open file and create reader
		with open("/home/keaton/.AF/%s.csv" % self.saveload.get(), 'rb') as f:
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
		for i in range(0,8):
			exec('self.answer'+str(i)+'.set(data[header[0]][i])')
			exec('self.point'+str(i)+'.set(data[header[1]][i])')
	
	def confirmit(self):
		self.t = Tkinter.Toplevel(self)
		self.t.wm_title("Are you sure")
		self.t.y = Tkinter.Button(self.t, text=u"Click to confirm save",command=self.saveit)
		self.t.y.grid(column=0,sticky='NSEW')
	
	def saveit(self):
		os.system("rm /home/keaton/.AF/%s.csv" % self.saveload.get())
		f = open("/home/keaton/.AF/%s.csv" % self.saveload.get(), 'a')
		f.write('"Answer","Points"\n')
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
		self.RedScore.set(self.RedScore.get()+self.Pot.get())
		self.Pot.set(0)

	def BlueAddPts(self):
		self.BlueScore.set(self.BlueScore.get()+self.Pot.get())
		self.Pot.set(0)
		
	def RedStrikeAdd(self):
		if self.RedStrike.get() == 'X X X':
			self.RedStrike.set('')
		elif self.RedStrike.get() == 'X X':
			self.RedStrike.set('X X X')
		elif self.RedStrike.get() == 'X':
			self.RedStrike.set('X X')
		else:
			self.RedStrike.set('X')
			
	def BlueStrikeAdd(self):
		if self.BlueStrike.get() == 'X X X':
			self.BlueStrike.set('')
		elif self.BlueStrike.get() == 'X X':
			self.BlueStrike.set('X X X')
		elif self.BlueStrike.get() == 'X':
			self.BlueStrike.set('X X')
		else:
			self.BlueStrike.set('X')

	####################################################################

	def MakeBoard(self):
		if self.BoardMaker.config('relief')[-1] == 'sunken':
			self.Pot.set(0)
			self.RedScore.set(0)
			self.BlueScore.set(0)
			self.RedStrike.set('')
			self.BlueStrike.set('')
			self.ShowWindow.destroy()
			self.BoardMaker.config(relief="raised",text=u"Create a new board")
		else:
			self.BoardMaker.config(relief="sunken",text=u"Close board")
			self.ShowWindow = Tkinter.Toplevel(self)
			self.ShowWindow.wm_grid()
			self.ShowWindow.wm_title("The Feud!")
			counter = 0
			#ROW0
			self.ShowWindow.RedScore = Tkinter.Label(self.ShowWindow,fg="white",bg="red",textvariable=self.RedScore)
			self.ShowWindow.RedScore.grid(column=0,columnspan=3,row=0,sticky="NSEW")
			self.ShowWindow.BlueScore = Tkinter.Label(self.ShowWindow,fg="white",bg="blue",textvariable=self.BlueScore)
			self.ShowWindow.BlueScore.grid(column=5,columnspan=3,row=0,sticky="NSEW")
			self.ShowWindow.Potbox = Tkinter.Label(self.ShowWindow,fg="white",bg="black",textvariable=self.Pot)
			self.ShowWindow.Potbox.grid(column=3,columnspan=2,row=0,rowspan=2,sticky="NSEW")
			#ROW1
			self.ShowWindow.RedStrikeCounter = Tkinter.Label(self.ShowWindow,bg="red",fg="white",textvariable=self.RedStrike)
			self.ShowWindow.RedStrikeCounter.grid(column=0,columnspan=3,row=1,sticky="NSEW")
			self.ShowWindow.BlueStrikeCounter = Tkinter.Label(self.ShowWindow,bg="blue",fg="white",textvariable=self.BlueStrike)
			self.ShowWindow.BlueStrikeCounter.grid(column=5,columnspan=3,row=1,sticky="NSEW")
			#ARRAYMAKER
			for i in range(0,8):
				checker = eval('app.answer'+str(i)+'.get()')
				if checker:
					counter = counter +1
					exec('self.ShowWindow.BoxLabel'+str(i)+' = Tkinter.StringVar()')
					exec('self.ShowWindow.BoxLabel'+str(i)+'.set(counter)')
					if i<4:
						exec('self.ShowWindow.Box'+str(i)+' = Tkinter.Label(self.ShowWindow,fg="white",bg="black",textvariable=self.ShowWindow.BoxLabel'+str(i)+')')
						exec('self.ShowWindow.Box'+str(i)+'.grid(column=0,columnspan=3,row='+str(i+2)+',sticky="NSEW")')
						exec('self.ShowWindow.BoxPnt'+str(i)+' = Tkinter.Label(self.ShowWindow,fg="white",bg="black")')
						exec('self.ShowWindow.BoxPnt'+str(i)+'.grid(column=3,row='+str(i+2)+',sticky="NSEW")')
					else:
						exec('self.ShowWindow.Box'+str(i)+' = Tkinter.Label(self.ShowWindow,fg="white",bg="black",textvariable=self.ShowWindow.BoxLabel'+str(i)+')')
						exec('self.ShowWindow.Box'+str(i)+'.grid(column=4,columnspan=3,row='+str(i-2)+',sticky="NSEW")')
						exec('self.ShowWindow.BoxPnt'+str(i)+' = Tkinter.Label(self.ShowWindow,fg="white",bg="black")')
						exec('self.ShowWindow.BoxPnt'+str(i)+'.grid(column=7,row='+str(i-2)+',sticky="NSEW")')
			#GEOMETRY
			for i in range(0,8):
				exec('self.ShowWindow.grid_columnconfigure('+str(i)+',weight=1)')
			for i in range(0,int(math.ceil(counter/2)+2)):
				if i < 2:
					exec('self.ShowWindow.grid_rowconfigure(0,weight=1)')
				else:
					exec('self.ShowWindow.grid_rowconfigure('+str(i)+',weight=2)')
			
			self.ShowWindow.resizable(True,True)
			self.ShowWindow.update()
			self.ShowWindow.geometry(self.ShowWindow.geometry())


if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title('Feud Control Center')
	app.mainloop()
