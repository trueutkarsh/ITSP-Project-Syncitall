#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
from PyQt4.QtGui import  *
from PyQt4.QtCore import *
class page(QWidget):
	def __init__(self,add):
		iconlist=[]
		super(page,self).__init__()
		self.setWindowTitle(add)
		self.resize(500,500)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(p)
	def initializelist(self,folderlist):
		pass
class icon(Qlabel):
	def __init__(self,page,name,imgadd):#decide whether you want to have a variable or just a common address
		super(foldericon,self).__init__(page)#each icon is associated with a page
		self.pic=QPixmap(imgadd)#to incude a pic pixmap
		self.setPixmap(self.pic)#pix map has been assighned its image
		self.foldername=QLabel(page)#label for the name of folder
		self.address=QString(name)#just for the sake of naming
		self.foldername.setText(name)#
		self.foldername.move(self.x()+self.width(),self.y()+self.pic.height()/2-10)#move text to appropriate height
		self.mousePressEvent = self.gotclicked
		self.foldername.mousePressEvent=self.gotclicked
		self.mouseDoubleClickEvent = self.gotdoubleclicked
		self.foldername.mouseDoubleClickEvent=self.gotdoubleclicked
		self.installEventFilter(self)
		

		#self.connect(self.foldername, SIGNAL('clicked()'), self.gotclicked)
	def move(self,x,y):#overwriting the existing function
		super(foldericon,self).move(x,y)
		self.foldername.move(self.x()+self.width(),self.y()+self.pic.height()/2-10)

	def gotclickedevent(self,event):
		#self.emit(QtCore.SIGNAL('clicked()'))
		if event.type()==QEvent.MouseButtonPress:
			if event.button()==Qt.LeftButton:
				self.leftclickevent()
				print("just got left clicked")
				#callfunction for left click on folder
				#since left click function has nothing special work to do even  if it is called with double click it won't matter
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
	pass
	#define leftclickevent,rightclickevent,doubleclickevent

class fileicon(icon):
	pass
	#define leftclickevent,rightclickevent,doubleclickevent



#class fileicon()
a=QApplication(sys.argv)
w=page("Documents")
b=foldericon(w,"Slides")
#w.resize(500,500)
#w.setWindowTitle("Hello World")
w.show()
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



		

