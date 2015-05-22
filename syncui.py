#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
from PyQt4.QtGui import  *
from PyQt4.QtCore import *
class page(QWidget):
	def __init__(self,add):
		super(page,self).__init__()
		self.windowtitle=add
		self.setWindowTitle(add)
		self.resize(500,500)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(p)
		self.iconlist=[]
class icon(QLabel):
	def __init__(self,page,name,imgadd):#decide whether you want to have a variable or just a common address
		super(icon,self).__init__(page)#each icon is associated with a page
		self.pic=QPixmap(imgadd)#to incude a pic pixmap
		self.setPixmap(self.pic)#pix map has been assighned its image
		self.foldername=QLabel(page)#label for the name of folder
		self.address=QString(name)#just for the sake of naming
		self.foldername.setText(name)#
		self.foldername.move(self.x()+self.width(),self.y()+self.pic.height()/2-10)#move text to appropriate height
		self.mousePressEvent = self.gotclickedevent
		self.foldername.mousePressEvent=self.gotclickedevent
		self.mouseDoubleClickEvent = self.gotclickedevent
		self.foldername.mouseDoubleClickEvent=self.gotclickedevent
		#self.installEventFilter(self)
		

		#self.connect(self.foldername, SIGNAL('clicked()'), self.gotclicked)
	def move(self,x,y):#overwriting the existing function
		super(icon,self).move(x,y)
		self.foldername.move(self.x()+self.width(),self.y()+self.pic.height()/2-10)

	def gotclickedevent(self,event):
		#self.emit(QtCore.SIGNAL('clicked()'))
		if event.type()==QEvent.MouseButtonPress:
			if event.button()==Qt.LeftButton:
				self.leftclickevent()
				print("just got left clicked")
				#callfunction for left click on folder
				#since left click function has nothing special work to do even  if it is called with double click it won't matter
				#STILL FIND A METHOD TO MAKE CLICK AND DOUBLECLICK ACTIONS SEPARATE
			elif event.button()==Qt.RightButton:
				print("just got right clicked")
				self.rightclickevent()
				#call function for right click on folder
		elif event.type()==QEvent.MouseButtonDblClick:
			self.doubleclickevent()
			print("just got double clicked")
	def leftclickevent(self):
		pass
	def rightclickevent(self):
		pass			
	def doubleclickevent(self):
		pass	
	def show(self):
		super(foldericon,self).show()
		self.foldername.show()	

		
class foldericon(icon):
	def __init__(self,page,name):
		super(icon,self).__init__(page,name,'/home/trueutkarsh/Pictures/downloadfolderfinal.png')

	#define leftclickevent,rightclickevent,doubleclickevent

class fileicon(icon):
	def __init__(self,page,name):
		super(icon,self).__init__(page,name,'/home/trueutkarsh/Pictures/document.png')	
	#define leftclickevent,rightclickevent,doubleclickevent
def makebrowser(address,folderpagelist,currpage):
	num=address.count('/')
	if num==1:#its a file
		tempfileicon=icon(currpage,address[1:],'/home/trueutkarsh/Pictures/document.png')#change here
		currpage.iconlist.append(tempfileicon)        
		return
	else:#its a folder
		add=address.strip()
		i=(add[1:]).find('/')
		name=add[1:i+1]
		print(name)
		remainingadd=add[i+1:]
		print(remainingadd)
		newpagename=currpage.windowtitle + name+'/'
		if newpagename not in folderpagelist.keys():
			temppage=page(newpagename)
			folderpagelist.update({newpagename:temppage})
		tempfoldicon=icon(currpage,name,'/home/trueutkarsh/Pictures/downloadfolderfinal.png') #change here
		currpage.iconlist.append(tempfoldicon)
		makebrowser(remainingadd,folderpagelist,folderpagelist[newpagename])	
			
  
#class fileicon()
a=QApplication(sys.argv)
w=page("/Home/")
#imgadd='/home/trueutkarsh/Pictures/downloadfolderfinal.png'
folderpagelist={}
folderpagelist.update({"/Home/":w})
makebrowser("/home/trueutkarsh/Pictures/downloadfolderfinal.png",folderpagelist,w)
for x,y in folderpagelist.items():
	y.show()	
#w.resize(500,500)
#w.setWindowTitle("Hello World")

#w.show()
sys.exit(a.exec_())

'''
import sys
from PyQt4.QtGui import *
 
# Create an PyQT4 application object.
a = QApplication(sys.argv)       
 
# The QWidget widget is the base class of all user interface objects in PyQt4.
w = QWidget()
 
# Set window size. 
w.resize(320, 240)
 
# Set window title  
w.setWindowTitle("Hello World!") 
 
# Show window
w.show() 
 
sys.exit(a.exec_())
'''



		

