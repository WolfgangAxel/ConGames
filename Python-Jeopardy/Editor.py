#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter,tkFont
import math
import glob
import os

class simpleapp_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		
	def initialize(self):
		self.grid()
		
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
			f.write("['A Category', 'A Question', 'An Answer', '']")
			f.close()
		self.ent=Tkinter.StringVar()
		self.Font = tkFont.Font(family="system",size=12)
		##############
		self.menya = Tkinter.Menu(self)
		self.menya.add_command(label="New", command=self.StartAnew)
		self.menya.OpenMenu = Tkinter.Menu(self.menya,tearoff=0)
		self.menya.savemen = Tkinter.Menu(self.menya,tearoff=0)
		self.menya.savemen.board=Tkinter.Menu(self.menya,tearoff=0)
		self.menya.savemen.board.add_command(label="Save to new file",command=self.RawSave)
		self.menya.savemen.forread=Tkinter.Menu(self.menya,tearoff=0)
		self.menya.savemen.forread.add_command(label="Save to new file",command=self.ReadSave)
		for i,name in enumerate(glob.glob(self.HOME+'/.PythonJeopardy/*.board')):
			if name:
				exec('def Open'+str(i)+'():'+
					'\n    app.OpenFile ="'+name+'"'+
					'\n    app.Round=1'+
					'\n    app.fileName = app.OpenFile.replace(app.HOME+"/.PythonJeopardy/","")'+
					'\n    app.fileName = app.fileName.replace(".board","")'+
					'\n    app.arrayload()')
				exec('self.menya.OpenMenu.add_command(label="'+name+'", command=Open'+str(i)+')')
				exec('def Save'+str(i)+'():'+
					'\n    app.SaveFile ="'+name+'"'+
					'\n    app.RawSave()')
				exec('self.menya.savemen.board.add_command(label="'+name+'", command=Save'+str(i)+')')
			else:
				self.OpenMenu.add_command(label="{None Found}")
		for i,name in enumerate(glob.glob(self.HOME+'/.PythonJeopardy/*.txt')):
			if name:
				exec('def SaveR'+str(i)+'():'+
					'\n    app.SaveFile ="'+name+'"'+
					'\n    app.ReadSave()')
				exec('self.menya.savemen.forread.add_command(label="'+name+'", command=SaveR'+str(i)+')')
		self.menya.add_cascade(label="Open",menu=self.menya.OpenMenu)
		self.menya.savemen.add_cascade(label="Save .board file", menu=self.menya.savemen.board)
		self.menya.savemen.add_cascade(label="Export Readable .txt File", menu=self.menya.savemen.forread)
		self.menya.Round = Tkinter.Menu(self.menya,tearoff=0)
		for Round in [1,2,3]:
			exec('self.menya.Round.add_command(label="Round '+str(Round)+'",command=self.loadround'+str(Round)+')')
		self.menya.add_cascade(label="Save",menu=self.menya.savemen)
		self.menya.add_cascade(label="Round",menu=self.menya.Round)
		self.menya.add_command(label="Change Point Values", command=self.pointass)
		self.menya.add_command(label="Auto Font Size",command=self.fontadj)
		self.config(menu=self.menya)
		##############
		for RND in ["R1","R2"]:
			exec('self.'+RND+'=Tkinter.Frame(self)')
			for cat in range(0,5):
				exec('self.'+RND+'.cat'+str(cat)+'=Tkinter.StringVar()')
				exec('self.'+RND+'.catscroll'+str(cat)+'=Tkinter.Scrollbar(self.'+RND+')')
				exec('self.'+RND+'.catlab'+str(cat)+' = Tkinter.Entry(self.'+RND+',textvariable=self.'+RND+'.cat'+str(cat)+',font=self.Font,width='+str(self.winfo_width()/5)+',xscrollcommand=self.'+RND+'.catscroll'+str(cat)+'.set)')
				exec('self.'+RND+'.catscroll'+str(cat)+'.config(command=self.'+RND+'.catlab'+str(cat)+'.xview)')
				exec('self.'+RND+'.catscroll'+str(cat)+'.grid()')
				exec('self.'+RND+'.catlab'+str(cat)+'.grid(column='+str(cat)+',row=0,sticky="NSEW")')
				for ques in range(1,6):
					exec('self.'+RND+'.box'+str(cat)+'x'+str(ques)+' = Tkinter.Button(self.'+RND+',command=self.reveal'+str(cat)+'x'+str(ques)+',font=self.Font,width='+str(self.winfo_width()/5)+')')
					exec('self.'+RND+'.box'+str(cat)+'x'+str(ques)+'.grid(column='+str(cat)+',row='+str(ques)+',sticky="NSEW")')
			for i in range(0,6):
				if i<5:
					exec('self.'+RND+'.grid_columnconfigure('+str(i)+',weight=1)')
				exec('self.'+RND+'.grid_rowconfigure('+str(i)+',weight=1)')
		
		self.R3 = Tkinter.Frame(self)
		##############
		self.StartAnew()
		
		self.grid_columnconfigure(0,weight=1)
		self.grid_rowconfigure(0,weight=1)
		self.resizable(True,True)
		self.update()
		self.geometry(self.geometry())
	
	####################################################################
		
	def savegame(self):
		self.savename = Tkinter.Toplevel(self)
		self.savename.wm_title("Enter a name to save the file as")
		self.savename.entbox=Tkinter.Entry(self.savename,textvariable=self.ent)
		self.savename.entbox.grid(column=0,row=0,sticky="NSEW")
		self.savename.proceed=Tkinter.Button(self.savename,text="Save",command=self.arraysave)
		self.savename.proceed.grid(column=1,row=0,sticky="NSEW")

	def arrayload(self):
		self.ent.set(self.fileName)
		f=open(self.OpenFile,'r')
		self.sepf = f.readlines()
		for Round in [1,2]:
			self.clusterfuck = {}
			self.clusterfuck = eval(str(self.sepf[Round-1]))
			self.P=eval(str(self.clusterfuck[1]))
			for cat in range(0,5):
				exec('self.R'+str(Round)+'.cat'+str(cat)+'.set("'+str(eval(str(eval(str(self.clusterfuck[0]))[cat]))[0])+'")')
				for ques in range(1,6):
					exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+' = Tkinter.Frame(self)')
					exec('self.R'+str(Round)+'.box'+str(cat)+'x'+str(ques)+'.config(text=eval(str(self.P['+str(ques-1)+'])))')
					##################################
					exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.imagefile = Tkinter.StringVar()')
					exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.imagecheck=Tkinter.Button(self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+',text="Add image",command=self.changerelief,font=self.Font)')
					exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.imagecheck.grid(row=1,column=2,sticky="NSEW")')
					for i,name in enumerate(["question","answer","image"]):
						if name == "image":
							if eval('str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))['+str(cat)+']))[1]))['+str(ques-1)+']))['+str(i)+'])'):
								self.CAT,self.QUES,self.Round=cat,ques,Round
								self.changerelief()
						else:
							exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.'+name+' = Tkinter.StringVar()')
							exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.'+name+'.set(str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))['+str(cat)+']))[1]))['+str(ques-1)+']))['+str(i)+']))')
							exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.'+name+'entry = Tkinter.Entry(self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+',textvariable=self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.'+name+',font=self.Font)')
							exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.'+name+'entry.grid(column='+str(i)+',row=0,sticky="NSEW")')
					exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.RtB=Tkinter.Button(self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+',text="Return to board",command=self.returntoboard,font=self.Font)')
					exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.RtB.grid(row=2,column=0,columnspan=3,sticky="NSEW")')
					for x in range(0,2):
						exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.columnconfigure('+str(x)+',weight=1)')
						exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.rowconfigure('+str(x)+',weight=1)')
					exec('self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.rowconfigure(2,weight=1)')
					##################################
		self.clusterfuck = {}
		self.clusterfuck = eval(str(self.sepf[2]))
		self.R3.category = Tkinter.StringVar()
		self.R3.category.set(self.clusterfuck[0])
		self.R3.categoryentry = Tkinter.Entry(self.R3,textvariable=self.R3.category,font=self.Font)
		self.R3.categoryentry.grid(column=0,columnspan=3,row=0,sticky="NSEW")
		for i,name in enumerate(["question","answer"]):
			exec('self.R3.'+name+' = Tkinter.StringVar()')
			exec('self.R3.'+name+'.set(self.clusterfuck['+str(i+1)+'])')
			exec('self.R3.'+name+'entry = Tkinter.Entry(self.R3,textvariable=self.R3.'+name+',font=self.Font)')
			exec('self.R3.'+name+'entry.grid(column='+str(i)+',row=1,sticky="NSEW")')
		self.R3.pointsentry = Tkinter.Label(self.R3,text="Final Jeopardy",font=self.Font)
		self.R3.pointsentry.grid(column=2,row=1,sticky="NSEW")
		self.R3.imagefile = Tkinter.StringVar()
		self.R3.imagecheck=Tkinter.Button(self.R3,text="Add image",command=self.changerelief,font=self.Font)
		if self.clusterfuck[3]:
			self.R3.imagecheck.config(relief="sunken")
		self.R3.imagefile.set(str(self.clusterfuck[3]))
		self.R3.imagecheck.grid(row=2,column=2,sticky="NSEW")
		for x in range(0,2):
			exec('self.R3.columnconfigure('+str(x)+',weight=1)')
			exec('self.R3.rowconfigure('+str(x)+',weight=1)')
		self.R3.rowconfigure(2,weight=1)
		self.Round = 1
		self.clusterfuck = eval(str(self.sepf[0]))
		self.P=eval(str(self.clusterfuck[1]))
		self.roundload()
		f.close()
		
	def roundload(self):
		exec('self.R'+str(self.Round)+'.grid(column=0,row=0,sticky="NSEW")')
		
	def RawSave(self):
		if self.SaveFile:
			self.fileName = self.SaveFile.replace(self.HOME+"/.PythonJeopardy/","")
			self.fileName = self.fileName.replace(".board","")
		self.ent.set(self.fileName)
		self.extension = ".board"
		self.newSaveName()
	
	def ReadSave(self):
		if self.SaveFile:
			self.fileName = self.SaveFile.replace(self.HOME+"/.PythonJeopardy/","")
			self.fileName = self.fileName.replace(".txt","")
		self.ent.set(self.fileName)
		self.extension = ".txt"
		self.newSaveName()
	
	def newSaveName(self):
		self.typebox = Tkinter.Toplevel(self)
		self.typebox.label = Tkinter.Label(self.typebox,text="Save file at: %s/.PythonJeopardy/" % self.HOME,font=self.Font)
		self.typebox.label.grid(row=0,column=0,sticky="NSEW")
		self.typebox.entry = Tkinter.Entry(self.typebox,textvariable=self.ent)
		self.typebox.entry.grid(row=0,column=1,sticky="NSEW")
		self.typebox.labelEx = Tkinter.Label(self.typebox,text="%s" % self.extension)
		self.typebox.labelEx.grid(row=0,column=2,sticky="NSEW")
		self.typebox.button = Tkinter.Button(self.typebox,text="Save",command=self.preSave)
		self.typebox.button.grid(row=0,column=3,sticky="NSEW")
		self.typebox.update()
		self.typebox.geometry(self.typebox.geometry())
		
	def preSave(self):
		self.fileName = self.ent.get() + self.extension
		self.startSave()
	
	def startSave(self):
		self.SaveFile = self.HOME + "/.PythonJeopardy/" + self.fileName
		self.arraysave()
		try:
			self.typebox.destroy()
		except:
			annoying = True
	
	def arraysave(self):
		f=open(self.SaveFile,'w')
		if self.fileName == self.fileName.replace(".txt",""):
			for Round in [1,2]:
				ABP=[]
				for cat in range(0,5):
					for ques in range(1,6):
						exec('q=self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.question.get()')
						q=q.replace('"','\"')
						q=q.replace("'","\'")
						exec('a=self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.answer.get()')
						a=a.replace('"','\"')
						a=a.replace("'","\'")
						exec('if self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.imagefile.get():'+
							'\n    if self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.imagefile.get() != "Type full path to image here":'
							'\n        i=self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.imagefile.get()'
							'\n    else:'+
							'\n        i=""'+
							'\nelse:'+
							'\n    i=""')
						i=i.replace('"','\"')
						i=i.replace("'","\'")
						exec('B'+str(ques)+'=[q,a,i]')
					exec('C'+str(cat)+'=[B1,B2,B3,B4,B5]')
					exec('ABP.append([self.R'+str(Round)+'.cat'+str(cat)+'.get(),C'+str(cat)+'])')
					Pn=[]
				for i,item in enumerate(self.P):
					Pn.append(item*Round)
				board = [ABP,Pn]
				f.write(str(board)+'\n')
			c=self.R3.category.get()
			c=c.replace('"','\"')
			c=c.replace("'","\'")
			q=self.R3.question.get()
			q=q.replace('"','\"')
			q=q.replace("'","\'")
			a=self.R3.answer.get()
			a=a.replace('"','\"')
			a=a.replace("'","\'")
			i=self.R3.imagefile.get()
			i=i.replace('"','\"')
			i=i.replace("'","\'")
			ABP=[c,q,a,i]
			f.write(str(ABP))
		else:
			################### I spent entirely too much time making this.
			f.writelines(	"                  ____ __  __ ______ __  __ ____   __  __"+"\n"+
							"                 /  O |\ \/ //_  __// /_/ // __ | /  \/ /"+"\n"+
							"                / ___/ _\  /  / /  / __  // /_/ // /\  /"+"\n"+
							"               /_/    /___/  /_/  /_/ /_/ |____//_/ /_/"+"\n"+
							"      ________ ______ ____     _____   ___      _____    _____  __    ___"+"\n"+
							"     /__   __//  ___//  _ \   /  __ \ /   |    /  __ \  /  __ \ \ \  /  /"+"\n"+
							"       /  /  /  /__ /  / | | /  /_/ |/  o |   /  /_/ | /  /  | | \ \/  /"+"\n"+
							"  __  /  /  /  ___//  / / / /  ____//  _  |  /  _   / /  /  / /_  \   /"+"\n"+
							" / /_/  /  /  /__ |  |_/ / /  /    /  / | | /  / | | /  /__/ /| |_/  /"+"\n"+
							" \_____/  /_____/  \____/ /__/    /__/  |_|/__/  |_|/_______/  \____/"+"\n\n\n")
			for Round in [1,2,3]:
				if Round <3:
					f.writelines("        X><><><><><><><><X\n        X    Round #%s    X\n        X><><><><><><><><X\n\n" % Round)
					for cat in range(0,5):
						exec('f.writelines("Category: "+self.R'+str(Round)+'.cat'+str(cat)+'.get()+"\\n")')
						for ques in range(1,6):
							exec('f.writelines(str(self.P['+str(ques-1)+']*'+str(Round)+')+": "+self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.question.get()+"\\n")')
							exec('f.writelines("    Answer: "+self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.answer.get()+"\\n")')
							exec('if self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.imagefile.get():'+
								'\n    if self.ed'+str(cat)+'x'+str(ques)+'R'+str(self.Round)+'.imagefile.get() != "Type full path to image here":'
								'\n        f.writelines("    Image: "+self.ed'+str(cat)+'x'+str(ques)+'R'+str(Round)+'.imagefile.get()+"\\n")')
						f.writelines("\n")
				else:
					f.writelines("        X><><><><><><><><X\n        X FINAL JEOPARDY X\n        X><><><><><><><><X\n\nCategory: %s\n    Question: %s\n    Answer: %s" % (self.R3.category.get(),self.R3.question.get(),self.R3.answer.get()))
					if self.R3.imagefile.get():
						if self.R3.imagefile.get() != "Type full path to image here":
							f.writelines("\n    Image: %s" % self.R3.imagefile.get())
		f.close()
	
	def pointass(self):
		self.pointbox = Tkinter.Toplevel(self)
		self.pointbox.wm_title("Enter point values")
		self.pointbox.menya = Tkinter.Menu(self.pointbox)
		self.pointbox.menya.add_command(label="Update Points", command=self.pointsave)
		self.pointbox.menya.add_command(label="Close", command=self.annoying)
		self.pointbox.config(menu=self.pointbox.menya)
		for i in range(0,5):
			exec('self.pointbox.points'+str(i)+'=Tkinter.IntVar()')
			exec('self.pointbox.points'+str(i)+'entry=Tkinter.Entry(self.pointbox,textvariable=self.pointbox.points'+str(i)+')')
			exec('self.pointbox.points'+str(i)+'entry.grid(column=0,row='+str(i)+',sticky="NSEW")')
		
	def annoying(self):
		self.pointbox.destroy()
		
	def pointsave(self):
		for i in range(1,6):
			for j in range(0,5):
				exec('self.P['+str(j)+']=int(self.pointbox.points'+str(j)+'entry.get())')
				exec('self.R'+str(self.Round)+'.box'+str(j)+'x'+str(i)+'.config(text=eval(str(self.P['+str(i-1)+']*'+str(self.Round)+')))')
			
	
	for Round in [1,2]:
		exec('def loadround'+str(Round)+'(self):'+
			'\n    exec("self.R"+str(self.Round)+".grid_remove()")'+
			'\n    self.clusterfuck = eval(str(self.sepf['+str(Round-1)+']))'+
			'\n    self.P=eval(str(self.clusterfuck[1]))'+
			'\n    self.Round = '+str(Round)+
			'\n    self.roundload()')
	def loadround3(self):
		exec("self.R"+str(self.Round)+".grid_remove()")
		self.clusterfuck = eval(str(self.sepf[2]))
		self.Round = 3
		self.roundload()
	
	def fontadj(self):
		ws=self.winfo_width()
		self.Font.config(size=int(math.ceil(ws/60)))
		if self.Round <3:
			for cat in range(0,5):
				for ques in range(1,6):
					exec('self.R'+str(self.Round)+'.box'+str(cat)+'x'+str(ques)+'.config(wraplength='+str(int(math.ceil(ws/5)))+')')
					exec('self.R'+str(self.Round)+'.catlab'+str(cat)+'.config(width='+str(int(math.ceil(ws/5)))+')')
	
	for cat in range(0,5):
		for ques in range(1,6):
			exec('def reveal'+str(cat)+'x'+str(ques)+'(self):'+
				'\n    self.CAT='+str(cat)+
				'\n    self.QUES='+str(ques)+
				'\n    self.PTS=self.P['+str(ques-1)+']'+
				'\n    self.reveal()')
				
	def reveal(self):
		exec('self.R'+str(self.Round)+'.grid_remove()')
		exec('self.ed'+str(self.CAT)+'x'+str(self.QUES)+'R'+str(self.Round)+'.pointsentry = Tkinter.Label(self.ed'+str(self.CAT)+'x'+str(self.QUES)+'R'+str(self.Round)+',text=eval(str(self.P['+str(self.QUES-1)+'])),font=self.Font)')
		exec('self.ed'+str(self.CAT)+'x'+str(self.QUES)+'R'+str(self.Round)+'.pointsentry.grid(column=2,row=0,sticky="NSEW")')
		exec('self.ed'+str(self.CAT)+'x'+str(self.QUES)+'R'+str(self.Round)+'.grid(row=0,column=0,sticky="NSEW")')
		
	def changerelief(self):
		if self.Round<3:
			exec('FRAME = "self.ed'+str(self.CAT)+'x'+str(self.QUES)+'R'+str(self.Round)+'"')
		else:
			FRAME = "self.R3"
		if eval(FRAME+'.imagecheck.config("relief")[-1]') == "raised":
			exec(FRAME+'.imagecheck.config(relief="sunken",text="Remove image")')
			exec('if not str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))['+str(self.CAT)+']))[1]))['+str(self.QUES-1)+']))[2]):'+
				'\n    '+FRAME+'.imagefile.set("Type full path to image here")'+
				'\nelse:'+
				'\n    '+FRAME+'.imagefile.set(str(eval(str(eval(str(eval(str(eval(str(self.clusterfuck[0]))['+str(self.CAT)+']))[1]))['+str(self.QUES-1)+']))[2]))')
			exec(FRAME+'.imageentry = Tkinter.Entry('+FRAME+',textvariable='+FRAME+'.imagefile,font=self.Font)')
			if self.Round<3:
				exec(FRAME+'.imageentry.grid(row=1,column=0,columnspan=2,sticky="NSEW")')
			else:
				exec(FRAME+'.imageentry.grid(row=2,column=0,columnspan=2,sticky="NSEW")')
		else:
			exec(FRAME+'.imagecheck.config(relief="raised",text="Add image")')
			exec(FRAME+'.imageentry.grid_remove()')
			exec(FRAME+'.imagefile.set("")')
			
	def returntoboard(self):
		exec('self.ed'+str(self.CAT)+'x'+str(self.QUES)+'R'+str(self.Round)+'.grid_remove()')
		exec('self.R'+str(self.Round)+'.grid(column=0,row=0,sticky="NSEW")')
	
	def StartAnew(self):
		self.OpenFile = self.HOME+"/.PythonJeopardy/Default"
		self.fileName=""
		self.SaveFile = ""
		self.arrayload()
		

if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title('Jeopardy Editor')
	app.mainloop()
