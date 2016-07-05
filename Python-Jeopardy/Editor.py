#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
import glob
import os

class simpleapp_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		
	def initialize(self):
		self.grid()
		
		if not os.path.exists(os.getcwd()+'/.PythonJeopardy'):
			os.mkdir(os.getcwd()+'/.PythonJeopardy')
		
		self.menya = Tkinter.Menu(self)
		self.menya.add_command(label="New", command=self.StartAnew)
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
		self.menya.add_command(label="Save", command=self.savegame)
		self.menya.add_command(label="Save Readable .txt File", command=self.savereadable)
		self.menya.add_command(label="Previous Category", command=self.prevcat)
		self.menya.add_command(label="Next Category", command=self.nextcat)
		self.menya.add_command(label="Change Point Values", command=self.pointass)
		self.config(menu=self.menya)
		
		for cat in range(0,5):
			exec('self.cat'+str(cat)+' = Tkinter.Frame(self)')
			exec('self.CatName'+str(cat)+'=Tkinter.StringVar()')
			exec('self.CatName'+str(cat)+'.set("Category '+str(cat+1)+'")')
			exec('self.CatNameBox'+str(cat)+'=Tkinter.Entry(self.cat'+str(cat)+',textvariable=self.CatName'+str(cat)+')')
			exec('self.CatNameBox'+str(cat)+'.grid(row=0,column=0,sticky="NSEW")')
			for x in range(0,6):
				exec('self.cat'+str(cat)+'.rowconfigure('+str(x)+',weight=1)')
			exec('self.cat'+str(cat)+'.columnconfigure(0,weight=1)')
			for ques in range(1,6):
				exec('self.points'+str(ques)+' = Tkinter.IntVar()')
				exec('self.cat'+str(cat)+'.entrybox'+str(ques)+' = Tkinter.Frame(self.cat'+str(cat)+')')
				exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.grid(row='+str(ques)+',column=0,sticky="NSEW")')
				for i,name in enumerate(["question","answer","points"]):
					if name == "points":
						exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.'+name+'entry = Tkinter.Label(self.cat'+str(cat)+'.entrybox'+str(ques)+',textvariable=self.'+name+str(ques)+')')
					else:
						exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.'+name+' = Tkinter.StringVar()')
						exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.'+name+'.set("'+name+'")')
						exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.'+name+'entry = Tkinter.Entry(self.cat'+str(cat)+'.entrybox'+str(ques)+',textvariable=self.cat'+str(cat)+'.entrybox'+str(ques)+'.'+name+')')
					exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.'+name+'entry.grid(column='+str(i)+',row=0,sticky="NSEW")')
				exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.imagefile = Tkinter.StringVar()')
				exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.imagecheck=Tkinter.Button(self.cat'+str(cat)+'.entrybox'+str(ques)+',text="Add image",command=lambda : changerelief('+str(cat)+','+str(ques)+'))')
				exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.imagecheck.grid(row=1,column=2,sticky="NSEW")')
				for x in range(0,2):
					exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.columnconfigure('+str(x)+',weight=1)')
					exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.rowconfigure('+str(x)+',weight=1)')
		
		self.ActiveFrame=0
		exec('self.cat'+str(self.ActiveFrame)+'.grid(sticky="NSEW")')
		for typ in ["column","row"]:
			exec('self.'+typ+'configure(0,weight=1)')
		self.resizable(True,True)
		self.update()
		self.geometry(self.geometry())
		
	def savegame(self):
		self.savename = Tkinter.Toplevel(self)
		self.savename.wm_title("Enter a name to save the file as")
		self.savename.ent=Tkinter.StringVar()
		self.savename.entbox=Tkinter.Entry(self.savename,textvariable=self.savename.ent)
		self.savename.entbox.grid(column=0,row=0,sticky="NSEW")
		self.savename.proceed=Tkinter.Button(self.savename,text="Save",command=self.arraysave)
		self.savename.proceed.grid(column=1,row=0,sticky="NSEW")

	def arrayload(self):
		f=open(self.OpenFile,'r')
		clusterfuck = {}
		clusterfuck = eval(str(f.read()))
		for cat in range(0,5):
			exec('self.CatName'+str(cat)+'.set(str(eval(str(eval(str(clusterfuck[0]))['+str(cat)+']))[0]))')
			for ques in range(1,6):
				exec('self.points'+str(ques)+'.set(eval(str(clusterfuck[1]))['+str(ques-1)+'])')
				for i,name in enumerate(["question","answer","image"]):
					if name == "image":
						if eval('str(eval(str(eval(str(eval(str(eval(str(clusterfuck[0]))['+str(cat)+']))[1]))['+str(ques-1)+']))['+str(i)+'])'):
							exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.imagecheck.config(relief="raised")')
							changerelief(cat,ques)
							exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.imagefile.set(str(eval(str(eval(str(eval(str(eval(str(clusterfuck[0]))['+str(cat)+']))[1]))['+str(ques-1)+']))['+str(i)+']))')
						else:
							exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.imagefile.set("")')
					else:
						exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.'+name+'.set(str(eval(str(eval(str(eval(str(eval(str(clusterfuck[0]))['+str(cat)+']))[1]))['+str(ques-1)+']))['+str(i)+']))')
		f.close()
	
	def arraysave(self):
		f=open(os.getcwd()+'/%s.board' % self.savename.ent.get(),'w')
		P=[]
		ABP=[]
		for cat in range(0,5):
			for ques in range(1,6):
				exec('q=self.cat'+str(cat)+'.entrybox'+str(ques)+'.question.get()')
				q=q.replace('"','\"')
				q=q.replace("'","\'")
				exec('a=self.cat'+str(cat)+'.entrybox'+str(ques)+'.answer.get()')
				a=a.replace('"','\"')
				a=a.replace("'","\'")
				exec('i=self.cat'+str(cat)+'.entrybox'+str(ques)+'.imagefile.get()')
				i=i.replace('"','\"')
				i=i.replace("'","\'")
				exec('B'+str(ques)+'=[q,a,i]')
				if cat == 0:
					exec('P.append(self.points'+str(ques)+'.get())')
			exec('C'+str(cat)+'=[B1,B2,B3,B4,B5]')
			exec('ABP.append([self.CatName'+str(cat)+'.get(),C'+str(cat)+'])')
		board = [ABP,P]
		f.write(str(board))
		f.close()
		self.savename.destroy()
		
	def prevcat(self):
		exec('self.cat'+str(self.ActiveFrame)+'.grid_remove()')
		if self.ActiveFrame==0:
			self.ActiveFrame=4
		else:
			self.ActiveFrame=self.ActiveFrame-1
		exec('self.cat'+str(self.ActiveFrame)+'.grid(sticky="NSEW")')
		for ques in range(1,6):
			exec('self.cat'+str(self.ActiveFrame)+'.entrybox'+str(ques)+'.pointsentry.config(textvariable=self.points'+str(ques)+')')
				
	def nextcat(self):
		exec('self.cat'+str(self.ActiveFrame)+'.grid_remove()')
		if self.ActiveFrame==4:
			self.ActiveFrame=0
		else:
			self.ActiveFrame=self.ActiveFrame+1
		exec('self.cat'+str(self.ActiveFrame)+'.grid(sticky="NSEW")')
		for ques in range(1,6):
			exec('self.cat'+str(self.ActiveFrame)+'.entrybox'+str(ques)+'.pointsentry.config(textvariable=self.points'+str(ques)+')')
	
	def pointass(self):
		self.pointbox = Tkinter.Toplevel(self)
		self.pointbox.wm_title("Enter point values")
		self.pointbox.menya = Tkinter.Menu(self.pointbox)
		self.pointbox.menya.add_command(label="Save", command=self.pointsave)
		self.pointbox.menya.add_command(label="Close", command=self.annoying)
		self.pointbox.config(menu=self.pointbox.menya)
		for i in range(0,5):
			exec('self.pointbox.points'+str(i)+'=Tkinter.IntVar()')
			exec('self.pointbox.points'+str(i)+'entry=Tkinter.Entry(self.pointbox,textvariable=self.pointbox.points'+str(i)+')')
			exec('self.pointbox.points'+str(i)+'entry.grid(column=0,row='+str(i)+',sticky="NSEW")')
			exec('self.cat'+str(self.ActiveFrame)+'.entrybox'+str(i+1)+'.pointsentry.config(textvariable=self.points'+str(i+1)+')')
		
	def annoying(self):
		self.pointbox.destroy()
		
	def pointsave(self):
		for i in range(1,6):
			exec('self.points'+str(i)+'.set(self.pointbox.points'+str(i-1)+'entry.get())')

	def savereadable(self):
		self.savename = Tkinter.Toplevel(self)
		self.savename.wm_title("Enter a name to save the file as")
		self.savename.ent=Tkinter.StringVar()
		self.savename.entbox=Tkinter.Entry(self.savename,textvariable=self.savename.ent)
		self.savename.entbox.grid(column=0,row=0)
		self.savename.proceed=Tkinter.Button(self.savename,text="Save",command=self.readablesave)
		self.savename.proceed.grid(column=1,row=0,sticky="NSEW")

	def readablesave(self):
		f=open(os.getcwd()+'/.PythonJeopardy/%s.txt' % self.savename.ent.get(),'w')
		for cat in range(0,5):
			exec('f.writelines("Category: "+self.CatName'+str(cat)+'.get()+"\\n")')
			for ques in range(1,6):
				exec('f.writelines(str(self.points'+str(ques)+'.get())+": "+self.cat'+str(cat)+'.entrybox'+str(ques)+'.question.get()+"\\n")')
				exec('f.writelines("    Answer: "+self.cat'+str(cat)+'.entrybox'+str(ques)+'.answer.get()+"\\n")')
				exec('f.writelines("    Image: "+self.cat'+str(cat)+'.entrybox'+str(ques)+'.imagefile.get()+"\\n")')
			f.writelines("\n")
		f.close()
		self.savename.destroy()
	
	def StartAnew(self):
		for cat in range(0,5):
			exec('self.CatName'+str(cat)+'.set("Category '+str(cat+1)+'")')
			for ques in range(1,6):
				exec('self.points'+str(ques)+'.set(0)')
				for i,name in enumerate(["question","answer"]):
					exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.'+name+'.set("'+name+'")')
				exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.imagefile.set("")')
				exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.imagecheck.config(relief="raised",text="Add image")')
				try:
					exec('self.cat'+str(cat)+'.entrybox'+str(ques)+'.imageentry.grid_remove()')
				except:
					ThisIsAnoying=0
				exec('self.cat'+str(self.ActiveFrame)+'.grid_remove()')
				self.cat0.grid(sticky="NSEW")
				self.ActiveFrame=0
					

def changerelief(cat,box):
	exec('FRAME="app.cat'+str(cat)+'.entrybox'+str(box)+'"')
	if eval(FRAME+'.imagecheck.config("relief")[-1]') != "sunken":
		exec(FRAME+'.imagecheck.config(relief="sunken",text="Remove image")')
		exec(FRAME+'.imagefile.set("Type full path to image here")')
		exec(FRAME+'.imageentry = Tkinter.Entry(app.cat'+str(cat)+'.entrybox'+str(box)+',textvariable=app.cat'+str(cat)+'.entrybox'+str(box)+'.imagefile)')
		exec(FRAME+'.imageentry.grid(row=1,column=0,columnspan=2,sticky="NSEW")')
	else:
		exec(FRAME+'.imagecheck.config(relief="raised",text="Add image")')
		exec(FRAME+'.imageentry.grid_remove()')
		exec(FRAME+'.imagefile.set("")')

if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title('Jeopardy Editor')
	app.mainloop()
