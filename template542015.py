import dropbox
import httplib2
import pprint
import time
import os
import shutil
import ntpath
#import urllib2
#libraries for gdrive file operations
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from apiclient import errors
from apiclient import http
#libraries for web browsing
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#libraries for address box
import Tkinter
import tkFileDialog
#libraries for onedrive file upload
import onedrive
import commands #to read output

#libraries for Tkinter dialog box
import Tkinter
import tkFileDialog
# main() function gets file directory through dialog box. 
#libraries for gui
import sys
from PyQt4.QtGui import  *
from PyQt4.QtCore import *

def main1():
	adda=QString()
	adda=str(QFileDialog.getExistingDirectory())
	return adda
	# main2() gets file name through dialog box.
def main2():
	addb=QString()
	addb=str(QFileDialog.getOpenFileName())
	return addb


class file:#bas class file
	authorized=False#whether authorization has taken place or not
	listupdated=False#whether file list is updated or not
	downloadfilepath=None
	#distributed
	def __init__(self,location):
		self.address=location#address of file on pc
		
	def upload(self):
		pass
	@staticmethod
	def authorize():
		pass

class gdrivefile(file):
	drive_service=None
	filelist=[]
	currentquota=None
	supportslargeupload=True
	maxupldsize=None

	def upload(self):
		if gdrivefile.authorized==False :
			gdrivefile.authorize()
			gdrivefile.authorized=True

		FILENAME = self.address
		media_body = MediaFileUpload(FILENAME, mimetype='', resumable=True)
		body = {
		  'title': ntpath.basename(FILENAME),
		  'description': '',
		  'mimeType': ''
		}
		try:
			file = gdrivefile.drive_service.files().insert(body=body, media_body=media_body).execute()
			#iINSERT CODE TO UPDATE FILE LIST
			gdrivefile.updatefilelist()
		except errors.HttpError,error :
			print("error in uploading file")	

		#pprint.pprint(file)

	@staticmethod
	def authorize():
		CLIENT_ID = '268285193546-qpu3mbasinue8ofpiah50fu928lcf24b.apps.googleusercontent.com'
		CLIENT_SECRET = '0iyrUyCs-MhAIyOMeYKeeQO-'

		# Check https://developers.google.com/drive/scopes for all available scopes
		OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

		# Redirect URI for installed apps
		REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

		flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
						   redirect_uri=REDIRECT_URI)
		authorize_url = flow.step1_get_authorize_url()
		#print 'Go to the following link in your browser: ' + authorize_url

		try:		
			driver=webdriver.Firefox()#depends on your browser
						
			driver.get(authorize_url)
			cookies=driver.get_cookies()
			for cookie in cookies:
				driver.add_cookie(cookie)			
			#login=driver.find_element_by_name("signIn")
			#login.send_keys(Keys.RETURN)
			accept= WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "submit_approve_access")))
			accept.send_keys(Keys.RETURN)
				#accept.click()
			a=WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "code")))
				
			code=a.get_attribute('value')		
			driver.quit()
			gdrivefile.authorized=True
		except:
			print "Could not authorize to Google Drive"
			return None
		#code = raw_input('Enter verification code: ').strip()#change here
		credentials = flow.step2_exchange(code)

		# Create an httplib2.Http object and authorize it with our credentials
		http = httplib2.Http()
		http = credentials.authorize(http)

		gdrivefile.drive_service = build('drive', 'v2', http=http)
	@staticmethod
	def updatefilelist():#information about files on your drive
		if gdrivefile.authorized==False :
			return None
		page_token = None
		while True:
			try:
				param={}
				if page_token:
					param['pageToken']=page_token
				dfiles=gdrivefile.drive_service.files().list(**param).execute()
				gdrivefile.filelist.extend(dfiles['items'])
				page_token=dfiles.get('nextPageToken')
				gdrivefile.listupdated=True
				if not page_token:
					break
			except errors.HttpError:
				print("error in udating list")
				break
	'''			
	@staticmethod
	def getfile():
		if gdrivefile.listupdated==False:
			gdrivefile.updatefilelist()
		ref=[]	
		sample=raw_input('enter the file name ').strip()
		for gfile in gdrivefile.filelist:#change here
			if sample in gfile['title']:
				if sample==gfile['title']:
					return gfile
				ref.append(gfile['title'])
		print("No match found.Following are the related files")
		for name in ref:
			print(name)	
		return None				
	'''	
	#NO USE OF IT SINCE
					
	def download(self,add=None):
		if gdrivefile.listupdated==False:
			gdrivefile.updatefilelist()
		gdrivefile.listupdated=True
		file2download=None
		if '/' in self.address:
			i=self.address.rfind('/')
			filename=self.address[i+1:]
		else:
			filename=self.address			
		for a in gdrivefile.filelist:
			if a['title']==filename:
				file2download=a
				break
		if file2download==None:
			return
		else:
			downloadedfile=open(file2download.get('title'),"wb")

			download_url=file2download.get('downloadUrl')
			if download_url:
				resp ,content=gdrivefile.drive_service._http.request(download_url)
				if resp.status==200:
					#print('Status',resp)
					downloadedfile.write(content)
					if add==None:#change here
						add2=main1()
					add2=add	
					src=add2+"/"+ file2download.get('title')
					dest=os.getcwd()+"/"+ file2download.get('title')
					#shutil.move(dest,src)	


					downloadedfile.close()
					#os.rename(dest,src)
					shutil.move(dest,src)
					
				else :
					print("An error occured in downloading")
			else:
				print("No such file exists ")

	@staticmethod
	def getquota():
		if gdrivefile.authorized==False :
			gdrivefile.authorize()
			gdrivefile.authorized=True
		about=gdrivefile.drive_service.about().get().execute()	
		gdrivefile.currentquota=[int(about['quotaBytesTotal']),int(about['quotaBytesTotal'])-int(about['quotaBytesUsed'])]
	@staticmethod
	def makefinallist(finallist,filelist):

		for name in filelist:
			tmpgdrivefile=gdrivefile(name['title'])
			finallist.update({str(name['title']):tmpgdrivefile})
						
class odrivefile(file):
	filelist=None
	currentquota=None
	supportslargeupload=False
	maxupldsize=90*1024*1024
	def upload(self):#problem-provided method does'nt allows upload of files with path name having spaces
		#code for upload
		if odrivefile.authorized ==False:
			odrivefile.authorize()
			odrivefile.authorized=True
		try :
			 	
			#if ' ' not in self.address:#soln 1-no space in address upload the thing directly
			os.system("onedrive-cli put '"+self.address+"'")
			#	return
			#else
			'''	
			l=self.address.rfind('/')
			name=self.address[l+1:].strip()
			folder=self.address[:l+1]
			name2=name.replace(" ","\ ")
			#os.rename(folder+name,folder+name2)
			self.address=folder+name2
			print(name2)
			src=self.address
			print(src)
			dest=os.getcwd()+'/'+name2
			print(dest)
		
			os.rename(src,dest)
			os.system("onedrive-cli put "+name2)
			os.rename(dest,src)
			return
			'''
		except Exception ,e:
			print(str(e))
			print("error in uploading one drive file")	

	@staticmethod
	def authorize():
		#code for authorization
		'''
		client_id='000000004015642C'
		driver=webdriver.Firefox()
		client_secret='w2A-Ass34UsVdS16PqibDAOmgTdddlTZ'
		
		oredirecturi= 'https://login.live.com/oauth20_desktop.srf'
		startauturl='https://login.live.com/oauth20_authorize.srf?client_id='+client_id+'&scope='+ oscope+ '%20wl.basic&response_type=code&redirect_uri='+oredirecturi
		driver.get(startauturl)
		'''
		try:

			oscope='onedrive.readwrite'#scope=how do u want to get access(PROBLEM HERE)=REQUESTED SCOPE DOES'NT MATCHES GIVEN SCOPE
			driver=webdriver.Firefox()
			authurl= 'https://login.live.com/oauth20_authorize.srf?scope='+oscope+'&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf&response_type=code&client_id=000000004015642C'
			driver.get(authurl)
			accept= WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "idBtn_Accept")))
			accept.send_keys(Keys.RETURN)
			endurl=str(driver.current_url)
			driver.quit()
			os.system("onedrive-cli auth "+ endurl)
			odrivefile.authorized=True
		except:
			print("Could'nt authorize onedrive")
			return None	
	@staticmethod	
	def updatefilelist():
		if odrivefile.authorized ==False:
			odrivefile.authorize()
			odrivefile.authorized=True

		templist=commands.getstatusoutput('onedrive-cli ls')[1].strip()
		odrivefile.filelist=templist.split('\n')
		for x in range(len(odrivefile.filelist)):
			odrivefile.filelist[x]=odrivefile.filelist[x][2:]

		
		odrivefile.listupdated=True
		#print(odrivefile.filelist)


	@staticmethod
	def onedrivequota():
		if odrivefile.authorized ==False:
			odrivefile.authorize()
			odrivefile.authorized=True
		x=commands.getstatusoutput('onedrive-cli quota')[1].strip().split('\n')
		a=x[0].find(':')
		free=x[0][a+2:]
		b=x[1].find(':')
		total=x[1][b+2:]
		if free[-1]=='G':
			free=int(float(free[:-1]))*1024*1024*1024
		elif free[-1]=='M':
			free=int(float(free[:-1]))*1024*1024
			
		odrivefile.currentquota=[int(float(total[:-1]))*1024*1024*1024,free]
		


		'''
		FOR ONEDRIVE FILES GET FILE FUNCTION AND DOWNLOAD FUNCTIONS HAVE BEEN MERGED 
		BECAUSE I COUDNT PASS THE VARIABLE BY REFERENCE.
		FIND SOME METHOD TO DO SO AND 
			@staticmethod
			def getfile():
				if odrivefile.listupdated==False:
					odrivefile.updatefilelist()
				oname=raw_input('Enter file name or some reference :').strip()
				if oname in odrivefile.filelist:
					filename=oname#make changes here
				else:
					ref=[]
					for entry in odrivefile.filelist:
						if oname in entry:
							ref.append(entry)
					if ref==[]:
						print("No match for your search")
					else:
						print('May be you were looking for:')
						for	x in ref:
							print(x)
					odrivefile.getfile(filename)			
		'''
	#@staticmethod
	#CHANGES TO BE MADE HERE
	def download(self,add=None):
		if odrivefile.listupdated==False:
			odrivefile.updatefilelist()
			odrivefile.listupdated=True
		'''	
		oname=raw_input('Enter file name or some reference :').strip()
		if oname in odrivefile.filelist:
			filename=oname#make changes here
			print("this is the file name "+ filename)
		'''	
		if '/' in self.address:
			i=self.address.rfind('/')
			filename=self.address[i+1:]
		else:
			filename=self.address	
		downloadedfile=open(filename,"wb")#open the final file
		#ofile2download=raw_input("Enter address of file on one drive with format folder1/folder2..../filename").strip()
		ofile2download=self.address
		#make something so it can get to his file easily(presently avoid folders)
		tempcontent=commands.getstatusoutput("onedrive-cli get '"+filename+"'")
		downloadedfile.write(tempcontent[1])
		src=os.getcwd()+'/'+filename
		if add==None:#chnge here
			d=main1()
		else:
			d=add	
		if d=='d':
			d=odrivefile.downloadfilepath
		d=d+'/'+filename	
		os.rename(src,d)
		downloadedfile.close()			
		'''	
		else:
			ref=[]
			for entry in odrivefile.filelist:
				if oname in entry:
					ref.append(entry)
			if ref==[]:
				print("No match for your search")
			else:
				print('May be you were looking for:')
				for	x in ref:
					print(x)
			odrivefile.download()
		'''	
	@staticmethod
	def printfilelist():
		if odrivefile.listupdated==False:
			odrivefile.updatefilelist()
			odrivefile.listupdated=True	
		for ofile in odrivefile.filelist:
			print(ofile)
	@staticmethod
	def getinfo(name):
		
		'''
		namestrt=tempcontent.find('name:')
		namend=tempcontent[namestrt:].find('\n')
		name=tempcontent[namestrt:namend].strip()
		'''
		typestrt=tempcontent.find('type:')
		typend=tempcontent[typestrt:].find('\n')
		filetype=tempcontent[typestrt+5:typend].strip()
		return filetype

	@staticmethod
	def makefinallist(finallist,filelist,folderlist):#since strings are immutable they cannot be changed,list being mutable can be modified.
		#eachelement of list is folder's name in hiearchial folder
		#odrivefile.updatefilelist()
		
		for name in filelist:
			#name.replace(' ','\ ')
			tempcontent=commands.getstatusoutput("onedrive-cli info '"+name+"'")[1]
			#print(tempcontent)
			
			typestrt=tempcontent.find('type:')
			typend=tempcontent[typestrt:].find('\n')
			filetype=tempcontent[typestrt+6:typestrt+typend].strip()
			print(filetype)
			#print('PROBLEM HERE')			
			if filetype=='folder' or filetype=='album':
				folderlist.append(name+'/')
				for x in folderlist:
					foldername=foldername+x
				print(foldername)
				foldername.strip()	
					
				templistcontent=commands.getstatusoutput("onedrive-cli ls '" + foldername[:-1] +"'")[1]
				templist=templistcontent.split('\n')
				for x in range(len(templist)):
					templist[x]=templist[x][2:]
				for x in templist:
					print(foldername+x)					
				odrivefile.makefinallist(finallist,templist,folderlist)
			else:
				foldername='/'
				for x in folderlist:
					foldername=foldername+x
				tmpodrivefile=odrivefile(foldername+name)
				#y={name:tmpodrivefile}
				finallist.update({name:tmpodrivefile})
								
					
		if folderlist!=[]:	
			folderlist.pop()		
									
class dropboxfile(file):
	client=None
	account=None
	currentquota=None
	supportslargeupload=True
	maxupldsize=None
	def upload(self):
		
		if dropboxfile.authorized==False :
			dropboxfile.authorize()
			dropboxfile.authorized=True
		#code for upload
		a=self.address.rfind('/')
		name=self.address[a+1:]
		f = open(self.address, 'rb')
		response = dropboxfile.client.put_file(ntpath.basename(self.address), f)

	@staticmethod
	def authorize():
		app_key = '0iwzfwq43mcvirb'
		app_secret = 'ivcutlb76xs5cbr'
	
		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
		authorize_url = flow.start()
		try:
			driver=webdriver.Firefox()#depends on your browser
			
			driver.get(authorize_url)
			#login=driver.find_element_by_name("signIn")
			#login.send_keys(Keys.RETURN)
			accept= WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.NAME, "allow_access")))
			accept.send_keys(Keys.RETURN)
				#accept.click()
			#code=find_element_by_id("auth-code").get_attribute("innerHTML")
			code=WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "auth-code"))).get_attribute("innerHTML")
				
				
			driver.quit()
			dropboxfile.authorized=True
		except:
			print "Could not authorize to dropbox"
			return None
		dropbox.access_token, dropbox.user_id = flow.finish(code)
		dropboxfile.client = dropbox.client.DropboxClient(dropbox.access_token)
		dropboxfile.account=dropboxfile.client.account_info()
		#code for authorization	
	
	def download(self,add=None):
		if dropboxfile.authorized==False :
			return None
		try:
			if '/' in self.address:
				i=self.address.rfind('/')
				filename=self.address[i+1:]
			else:
				filename=self.address			
			f, metadata = dropboxfile.client.get_file_and_metadata(filename)
		except TypeError:
			file.found=0
		if add==None:#change here	
			add=main1()
				
		
		out = open(add+"/"+ntpath.basename(filename), 'wb')
		out.write(f.read())
		out.close()
	@staticmethod
	def makefilelist(add,finallist):
		if dropboxfile.authorized==False:
			return None
		folder_metadata = dropboxfile.client.metadata(add)
		#print folder_metadata

		for x in folder_metadata['contents']:
			if x['is_dir']==False:
				
				
				tmpdrpfile=dropboxfile(x['path'])
				finallist.update({ntpath.basename(x['path']):tmpdrpfile})
					
			else:
				add=x['path']+"/"
				dropboxfile.makefilelist(add,finallist)

	@staticmethod
	def quota():
		if dropboxfile.authorized==None:
			print "Dropbox not authorized"
			return None
		else:
			print ("shared : " +str(dropboxfile.account['quota_info']['shared']))
			print ("quota : " +str(dropboxfile.account['quota_info']['quota']))
			print ("normal : " +str(dropboxfile.account['quota_info']['normal']))	
		currentquota=(int(dropboxfile.account['quota_info']['normal']),int(dropboxfile.account['quota_info']['normal'])-int(dropboxfile.account['quota_info']['quota']))
	@staticmethod
	def printlist(add):
		if dropboxfile.authorized==False:
			return None
		folder_metadata = dropboxfile.client.metadata(add)
		#print folder_metadata

		for x in folder_metadata['contents']:
			if x['is_dir']==False:
				print ntpath.basename(x['path'])
				
				
					
			else:
				add=x['path']+"/"
				dropboxfile.printlist(add)
				
class FinalList:
	def __init__(self):
		self.finallist={}
	def update(self):
		gdrivefile.authorize()
		odrivefile.authorize()
		dropboxfile.authorize()
		gdrivefile.updatefilelist()
		odrivefile.updatefilelist()
		add='/'
		#dropboxfile.makefilelist(add,self.finallist)
		folder=[]
		#odrivefile.makefinallist(self.finallist,odrivefile.filelist,folder)
		#gdrivefile.makefinallist(self.finallist,gdrivefile.filelist)
	def printaddress(self):
		for a,b in self.finallist.items():
			print(a,str(b.address))#change here
	def download(self,filename):
		#filename=raw_input("Name of file").strip()
		self.finallist[filename].download()		
'''--------------------CODE FOR GUI STARTS HERE---------------------------'''					
main=None
abc=QApplication(sys.argv)

class page(QWidget):
	def __init__(self,add):
		super(page,self).__init__()
		self.windowtitle=add
		self.setWindowTitle(add)
		self.address=add
		self.resize(500,500)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(p)
		self.iconlist=[]
	def newfolder(self):
		tmpfolder=foldericon(self,"Untitled")
		tmpfolder.is_new=True
		self.iconlist.append(tmpfolder)
		yo(folderpagelist,self.windowtitle)
		#code for context menu

		#self.movelist=[]
	def cut(self,icon):#page from where stuff will be copied
		main.movelist.append(icon)
		self.iconlist.remove(icon)
		yo(folderpagelist,self.address)
		#main.update(folderpagelist,self.address)
	def paste(self):
 		if main.movelist != []:
				self.iconlist=main.movelist+self.iconlist
			#main.update(folderpagelist,self.address)
				yo(folderpagelist,self.address)#modifies the page..
				del main.movelist[:]
	def newfile(self,filename):
		tempfileicon=fileicon(self,filename)
		self.iconlist.append(tempfileicon)
		yo(folderpagelist,self.address)

		 
def yo(folderpagelist,address):
	main.clear(main.mainLayout)
	#main.mainLayout.removeWidget(main.backbutton)
	#main.mainLayout.removeWidget(main.scroll)
	main.update(folderpagelist,address)
	main.show()

class icon(QLabel):
	def __init__(self,page,name,imgadd):#decide whether you want to have a variable or just a common address
		super(icon,self).__init__(page)#each icon is associated with a page
		self.icon2=QIcon()
		self.pic=QPixmap(imgadd)#to incude a pic pixmap
		self.icon2.addPixmap(self.pic,QIcon.Normal,QIcon.On)
		self.setPixmap(self.icon2.pixmap(128,QIcon.Normal,QIcon.On))#pix map has been assighned its image
		self.foldername=QLabel(page)#label for the name of folder
		self.address=QString(name)#just for the sake of naming
		self.page=page
		self.name=name
		self.foldername.setText(name)
		self.foldername.move(self.x()+self.width(),self.y()+self.pic.height()/2-10)#move text to appropriate height
		self.mousePressEvent = self.gotclickedevent
		self.foldername.mousePressEvent=self.gotclickedevent
		self.mouseDoubleClickEvent = self.gotclickedevent
		self.foldername.mouseDoubleClickEvent=self.gotclickedevent
		self.ad=page.windowtitle
		#self.installEventFilter(self)
		self.h=QVBoxLayout()
		
		
		self.txtlabel=QLabel()
		self.txtlabel.setToolTip(name)
		self.is_new=False
		self.new_label=QLineEdit()
		self.new_label.returnPressed.connect(self.new_fol)
		#txtlabel.setFixedSize(130,10)
		#txtlabel.setStyleSheet("QWidget {background-color:blue}")
		if len(name)>15:
			name=name[:11]+"..."
		self.txtlabel.setText(name)
		self.txtlabel.setFixedSize(130,20)
		self.txtlabel.setAlignment(Qt.AlignCenter)
		self.setAlignment(Qt.AlignCenter)
	def new_fol(self):
		self.new_label.hide()
		txt=self.new_label.text()
		self.name=str(txt)
		self.txtlabel.setText(self.name)
		new_page=page(self.page.windowtitle+self.name+"/")
		folderpagelist.update({self.page.windowtitle+self.name+"/":new_page})
		yo(folderpagelist,self.page.windowtitle)
		
		'''
	def hiddenname():
		i=15
		label=QVBoxLayout()
		label2=QLabel()
		while ((len(self.name)-15-i)>0):
			tmp=self.name[i:i+14]
			
			label2.setText(tmp)
			label.addWidget(label2)
			i=i+15
		label2.setText(self.name[i:])
		label.addWidget(label2)
		return label
		'''


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
		self.txtlabel.setText(self.name)
		pass
 
	def rightclickevent(self):
		pass			
	def doubleclickevent(self):
		'''
		main.clear(main.layout)
		main.update(folderpagelist,self.ad+self.name+"/")
		
		main.show() 
		'''

	def show(self):
		super(foldericon,self).show()
		self.foldername.show()  

class foldericon(icon):
	def __init__(self,page,name):
		super(foldericon,self).__init__(page,name,'/home/trueutkarsh/Pictures/downloadfolderfinal.png')
	def gotclickedevent(self,event):
		super(foldericon,self).gotclickedevent(event)
	def doubleclickevent(self):
		
		main.clear(main.mainLayout)
		#main.mainLayout.removeWidget(main.backbutton)
		#main.mainLayout.removeWidget(main.scroll)
		main.update(folderpagelist,self.ad+self.name+"/")
		main.show()
		main.curradd=self.ad+self.name+"/" 
	#define leftclickevent,rightclickevent,doubleclickevent

class fileicon(icon):
	def __init__(self,page,name):
		super(fileicon,self).__init__(page,name,'/home/trueutkarsh/Pictures/documents.jpg') 
	def contextMenuEvent(self, event):
		#index = self.indexAt(event.pos())
		self.menu = QMenu()
		renameAction = QAction('Exit',self)
		Download = QAction('Download',self)
		cut=QAction('Cut',self)
		paste=QAction('Paste',self)
		self.menu.addAction(paste)
		self.menu.addAction(Download)
		self.menu.addAction(cut)
		Download.triggered.connect(lambda x:File.download(self.name))
		cut.triggered.connect(lambda x:folderpagelist[main.curradd].cut(self))#change here
		paste.triggered.connect(lambda x:main.paste())
		self.menu.popup(QCursor.pos())

	#define leftclickevent,rightclickevent,doubleclickevent

def makebrowser(address,folderpagelist,currpage):
	num=address.count('/')
	if num==1:#its a file
		for i in currpage.iconlist:
			if i.name==address[1:]:
				return


		tempfileicon=fileicon(currpage,address[1:])#change here
		currpage.iconlist.append(tempfileicon)		
		return
	elif num==0:#its a file
		for i in currpage.iconlist:
			if i.name==address:
				return


		tempfileicon=fileicon(currpage,address)#change here
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
			tempfoldicon=foldericon(currpage,name) #change here
			currpage.iconlist.append(tempfoldicon)
		makebrowser(remainingadd,folderpagelist,folderpagelist[newpagename])	
			
class Main(QMainWindow):
	

	def __init__(self,folderpagelist,address,parent = None):
			super(Main, self).__init__(parent)
			self.centralWidget=QWidget()
			self.setCentralWidget(self.centralWidget)

			self.mainLayout=QGridLayout()
			self.container=QWidget()
			self.scroll=QScrollArea()
			self.layout=QGridLayout()
			self.backicon=QIcon()
			self.curradd=address
			self.movelist=[]
			a=QSize(90,90)
			self.backicon.addFile('back.png',a,QIcon.Normal,QIcon.On)
	def update(self,folderpagelist,address):
		tmplist={}
		for a,b in folderpagelist.items():
			tmplist.update({a:b})
		print address
		self.layout=QGridLayout()
		self.container=QWidget()
		self.scroll=QScrollArea()
		self.layout=QGridLayout()
		self.backbutton=QPushButton(self.backicon,"Back",self.centralWidget)
		self.backbutton.setFixedSize(60,24)
		self.backbutton.clicked.connect(self.lp)
		###
		folderpagelist[address].setLayout(self.layout)
		self.ad=address
		k=0
		j=0
		i=0
		self.positions=[]
		self.positions2=[]   
		while(i<len(folderpagelist[address].iconlist)):
			j=0
			while(j<4 and i<len(folderpagelist[address].iconlist )):
					
				self.positions=self.positions+[(k,j)]
				self.positions2=self.positions2+[(k+1,j)]
				j=j+1
				i=i+1
			k=k+1
			
			#pos1=QMouseEvent.pos()
			#m=QMouseEvent()
			
		for position,icon,position2 in zip(self.positions,folderpagelist[address].iconlist,self.positions2):
				
			'''
				h=QVBoxLayout()
				label=Newlabel()
				txtlabel=QLabel()
				txtlabel.setText("Documents")
				h.addWidget(txtlabel)
				label.position=position
				label.setPixmap(icon.pixmap(size,QIcon.Normal,state))
				QtCore.QObject.connect(label, QtCore.SIGNAL('clicked()'), label.lp)
				w.addWidget(label,*position)
				h.addStretch(1)
				w.addItem(h,*position)
			'''
			overall=QVBoxLayout()
			overall.addWidget(icon)
			if  icon.is_new==False:
				icon.h.addWidget(icon.txtlabel)
				overall.addWidget(icon.txtlabel)
			else:
				icon.h.addWidget(icon.new_label)
				overall.addWidget(icon.new_label)
				icon.is_new=False	

			#txtlabel.move(0,100)
			#self.h.addStretch(2)
	   
			#self.layout.addItem(self.h,*position2)

			#self.layout.addWidget(txtlabel)
			#icon.setFixedSize(130,20)  

			self.layout.addItem(overall,*position)

			
			
		self.container.setLayout(self.layout)
		
		self.scroll.setWidget(self.container)
		self.mainLayout.addWidget(self.backbutton)
		self.mainLayout.addWidget(self.scroll)
		self.centralWidget.setLayout(self.mainLayout)	
		#self.centralWidget.setMaximumSize(600,600)
		
	def lp(self):
		count=self.ad[:-1].count('/')
		if count>1:
			i=self.ad[:-1].rfind("/")
			yo(folderpagelist,self.ad[:i+1])
			self.curradd=self.ad[:i+1]
			print("curr add is" +self.curradd)
		else:
			print("You are in home directory")	
		#main.clear(main.layout)
		#main.update(folderpagelist,self.ad[:i+1])
		#main.show()



	def clear(self,layout):
		'''
		for i in reversed(range(self.layout.count())):
			self.layout.itemAt(i).widget().setParent(None)
		'''

		for i in reversed(range(layout.count())):
			item = layout.itemAt(i)

			if isinstance(item, QWidgetItem):

				item.widget().close()
			# or
			# item.widget().setParent(None)
			elif isinstance(item, QSpacerItem):
				pass
			# no need to do extra stuff
			else:

				self.clear(item.layout())

		# remove the item from layout
			layout.removeItem(item)
	def contextMenuEvent(self, event):
		#index = self.indexAt(event.pos())
		self.menu = QMenu()
		renameAction = QAction('Exit',self)
		paste=QAction('Paste',self)
		self.menu.addAction(paste)
		new = QAction('New Folder',self)
		uploadf=QAction('Upload File',self)
		print self.ad
		new.triggered.connect(folderpagelist[self.ad].newfolder)
		self.menu.addAction(new)
		self.menu.addAction(uploadf)		
		#Download.triggered.connect(lambda x:File.download(self.name))
		#cut.triggered.connect(lambda x:folderpagelist[main.curradd].cut(self))#change here
		uploadf.triggered.connect(lambda x:upload(storelist))
		paste.triggered.connect(lambda x:folderpagelist[main.curradd].paste())
		self.menu.popup(QCursor.pos())


def splitsizef(storelist,filesize):
	if storelist[0]>=100*1024*1024:
		return 90
	else:
		if storelist[0]==0:#maximum number of splits
			#storelist.sort()
			print(storelist)
			storelist=storelist[1:]
			print("storelist below")
			print(storelist)			
			b=splitsizef(storelist,filesize)
		elif int(filesize/storelist[0])>100:
			print(storelist)
			storelist.sort()
			storelist=storelist[1:]
			print("storelist below")
			print(storelist)
			b=splitsizef(storelist,filesize)			
		else:
			b=int(storelist[0]/(1024*1024))	
	return b		


def splitfile(fileadd,filename,splitsize):
	os.mkdir("largefile "+filename)#make a dir
	os.chdir(os.getcwd()+'/largefile '+filename)#move into it
	print(os.getcwd()+'/'+filename)
	dest=os.getcwd()+'/'+filename
	os.rename(fileadd,dest)#move file into it
	os.system("split -b"+str(splitsize)+"m '"+filename+"'")#split the file							
	os.rename(dest,fileadd)#move back the original file to is source
	dirlist=os.listdir(os.getcwd())#list of names of files

	for x in dirlist:
		os.rename(os.getcwd()+'/'+x,os.getcwd()+'/'+filename+'$'+x)#rename them so that they have individual identity 



class distributedfile():
	def __init__(self,filename):
		self.files=[]
		self.filename=filename
	def update(self,x):
		self.files.append(x)
	def download(self,addr=None):
		if addr==None:
			add=main1()
		else:
			add=addr	
		print("download will happen herer"+add)
		presentdir=os.getcwd()
		print("presently i am here"+ presentdir)
		os.chdir(add)
		tmpfolder=self.filename+" folder"
		os.mkdir(tmpfolder)
		os.chdir(add+'/'+tmpfolder)
		i=1
		for x in self.files:
			x.download(add+'/'+tmpfolder)
			print("downloadedfile file "+str(i))
			i=i+1
		dirlist=os.listdir(os.getcwd())
		print(dirlist)
		for x in dirlist:
			t=x.rfind('$')#rfind beacuse file can be multply splitted
			os.rename(os.getcwd()+'/'+x,os.getcwd()+'/'+x[t+1:])
		os.system("cat x* > '"+self.filename+"'")
		src=add+'/'+tmpfolder+'/'+self.filename
		dest=add+'/'+self.filename
		print(src,dest)
		os.rename(src,dest)
		os.chdir(add)
		shutil.rmtree(tmpfolder)
		os.chdir(presentdir)



def upload(storelist,addfile=None,bigdfile=None):
	if addfile==None:
		addfile=main2()#get file address
	filesize=int(os.path.getsize(addfile))#size of the file
	a=addfile.rfind('/')
	filename=addfile[a+1:]#filename
	print(filename)
	totalfreespace=sum(storelist)#count the total space
	print(totalfreespace)
	storelist.sort()
	#ssplitsize=2
	iscorrect=True
	isfilesplitted=False
	if 2>1:
		if filesize>totalfreespace:
			print("File size too large.Insufficient space")
			print("total spcae="+str(totalfreespace)+"filesize= "+str(filesize))
			iscorrect=False
		else:
			if filesize<=90*1024*1024 and filesize<odrivefile.currentquota[1]:
				dfile=odrivefile(addfile)
				dfile.upload()
				a=storelist.index(odrivefile.currentquota[1])
				odrivefile.currentquota[1]-=filesize
				storelist[a]=odrivefile.currentquota[1]
				#storelist[a]=odrivefile.currentquota[1]
				#code for making icon out of it and updating iconlist folderpagelist and
			else:
				if gdrivefile.currentquota[1]==max(storelist):
					if filesize<=gdrivefile.currentquota[1]:
						dfile=gdrivefile(addfile)
						dfile.upload()
						a=storelist.index(gdrivefile.currentquota[1])
						gdrivefile.currentquota[1]-=filesize
						storelist[a]=gdrivefile.currentquota[1]
						#a=storelist.find(gdrivefile.currentquota[1])
						#gdrivefile.currentquota[1]-=filesize
						#storelist[a]=gdrivefile.currentquota[1]
					else:
						print("upload of gdrive one")
						#split the file,distribute the data #1 2 4
						#storelist=[odrivefile.currentquota[1],gdrivefile.currentquota[1],dropboxfile.currentquota[1]]
						isfilesplitted=True
						storelist.sort()
						#splitfile(addfile,filename,splitsize(storelist,filesize))
						ssplitsize=splitsizef(storelist,filesize)#find the chunks into which file will uploaded
						print("splitsize determined="+str(ssplitsize))
						splitfile(addfile,filename,ssplitsize)#split the file
						print("file spltted")
						dirlist=os.listdir(os.getcwd())
						print(dirlist)
						dfile=distributedfile(filename)
						for y in dirlist:
							padd=os.getcwd()+'/'+y#partial adress
							print("padd adress determined'")
							print(padd)
							psize=int(os.path.getsize(padd))#partial size
							if psize<=gdrivefile.currentquota[1]:
								tmpgdrivefile=gdrivefile(padd)
								tmpgdrivefile.upload()
								print("some part uploaded")
								i=storelist.index(gdrivefile.currentquota[1])
								gdrivefile.currentquota[1]-=psize
								storelist[i]=gdrivefile.currentquota[1]	
								#update the store list
								dfile.update(tmpgdrivefile)
								print("dfile updated")
							elif psize<=odrivefile.currentquota[1]:
								tmpodrivefile=odrivefile(padd)
								tmpodrivefile.upload()
								a=storelist.index(odrivefile.currentquota[1])
								odrivefile.currentquota[1]-=psize
								storelist[a]=odrivefile.currentquota[1]
								dfile.update(tmpodrivefile)

							elif psize<=dropboxfile.currentquota[1]:
								tmpdropboxfile=dropboxfile(padd)
								tmpdropboxfile.upload()
								a=storelist.index(dropboxfile.currentquota[1])
								dropboxfile.currentquota[1]-=psize
								storelist[a]=dropboxfile.currentquota[1]	
								dfile.update(tmpdropboxfile)

							else:
								if dirlist!=[]:#file size coud'nt fit inside
									upload(storelist,padd,dfile)
								else:
									print("Unusual error please close the program and contact developers.")	
									iscorrect=False
							print("totalfreespace free space now is="+str(sum(storelist)))								
				elif dropboxfile.currentquota[1]==max(storelist):
					if filesize<=dropboxfile.currentquota[1]:
						dfile=dropboxfile(addfile)
						dfile.upload()
						a=storelist.index(dropboxfile.currentquota[1])
						dropboxfile.currentquota[1]-=filesize
						storelist[a]=dropboxfile.currentquota[1]					
					else:
						#split the file,distribute the data #1 2 4
						#storelist=[odrivefile.currentquota[1],gdrivefile.currentquota[1],dropboxfile.currentquota[1]]
						print("upload of dropdrive one")
						isfilesplitted=True
						storelist.sort()
						ssplitsize=splitsizef(storelist,filesize)
						print("splitsize determined="+str(ssplitsize))
						splitfile(addfile,filename,ssplitsize)
						print("filesplitted")
						dirlist=os.listdir(os.getcwd())
						print(dirlist)
						##--------MAKE SOMTHING TO DECIDE THE PRIORITY LIST---------------##
						dfile=distributedfile(filename)
						for m in dirlist:
							padd=os.getcwd()+'/'+m#partial adress
							psize=int(os.path.getsize(padd))#partial size
							if psize<=gdrivefile.currentquota[1]:
								tmpgdrivefile=gdrivefile(padd)
								tmpgdrivefile.upload()
								print("uploaded some gdrive parrt")
								a=storelist.index(gdrivefile.currentquota[1])
								gdrivefile.currentquota[1]-=psize
								storelist[a]=gdrivefile.currentquota[1]
								dfile.update(tmpgdrivefile)
							elif psize<=odrivefile.currentquota[1]:
								tmpodrivefile=odrivefile(padd)
								tmpodrivefile.upload()
								print("uploaded some odrive part")
								a=storelist.index(odrivefile.currentquota[1])
								odrivefile.currentquota[1]-=psize
								storelist[a]=odrivefile.currentquota[1]
								dfile.update(tmpodrivefile)
							elif psize<=dropboxfile.currentquota[1]:
								tmpdropboxfile=dropboxfile(padd)
								tmpdropboxfile.upload()
								a=storelist.index(dropboxfile.currentquota[1])
								dropboxfile.currentquota[1]-=psize
								storelist[a]=dropboxfile.currentquota[1]
								dfile.update(tmpdropboxfile)
							else:
								if dirlist!=[]:#file size coud'nt fit inside
									upload(storelist,padd,dfile)
								else:
									print("Unusual error please close the program and contact developers.")	
									iscorrect=False	
							print("totalfreespace free space now is="+str(sum(storelist)))											
				elif odrivefile.currentquota[1]==max(storelist):
					if filesize<=odrivefile.currentquota[1]:
						dfile=odrivefile(addfile)
						dfile.upload()
						odrivefile.currentquota[1]-=filesize
					else:
						print("upload of onedrive one")
						#split the file,distribute the data #1 2 4
						#storelist=[odrivefile.currentquota[1],gdrivefile.currentquota[1],dropboxfile.currentquota[1]]
						isfilesplitted=True
						storelist.sort()
						ssplitsize=splitsizef(storelist,filesize)
						print("splitsize determined="+str(ssplitsize))
						splitfile(addfile,filename,ssplitsize)
						dirlist=os.listdir(os.getcwd())
						##--------MAKE SOMTHING TO DECIDE THE PRIORITY LIST---------------##
						dfile=distributedfile(filename)
						for z in dirlist:
							padd=os.getcwd()+'/'+z#partial adress
							psize=int(os.path.getsize(padd))#partial size
							if psize<=gdrivefile.currentquota[1]:
								tmpgdrivefile=gdrivefile(padd)
								tmpgdrivefile.upload()
								a=storelist.index(gdrivefile.currentquota[1])
								gdrivefile.currentquota[1]-=psize
								storelist[a]=gdrivefile.currentquota[1]
								dfile.update(tmpgdrivefile)
							elif psize<=odrivefile.currentquota[1]:
								tmpodrivefile=odrivefile(padd)
								tmpodrivefile.upload()
								a=storelist.index(odrivefile.currentquota[1])
								odrivefile.currentquota[1]-=psize
								storelist[a]=odrivefile.currentquota[1]
								dfile.update(tmpodrivefile)

							elif psize<=dropboxfile.currentquota[1]:
								tmpdropboxfile=dropboxfile(padd)
								tmpdropboxfile.upload()
								a=storelist.index(dropboxfile.currentquota[1])
								dropboxfile.currentquota[1]-=psize
								storelist[a]=dropboxfile.currentquota[1]
								dfile.update(tmpdropboxfile)								
							else:
								if dirlist!=[]:#file size coud'nt fit inside
									upload(storelist,padd,dfile)
								else:
									print("Unusual error please close the program and contact developers.")	
									iscorrect=False	
	'''						print("totalfreespace free space now is="+str(sum(storelist)))		
	except Exception, e:
		print(str(Exception))
		print(str(e))
		print("Sorry the action was unsuccessful.File size could'nt be uploaded.Please free your drive or check your connection")
		iscorrect=False																	
	'''	
	if iscorrect:
		if isfilesplitted:	
			cfold=os.getcwd()		
			b=cfold.rfind('/')		
			ldir=cfold[:b]
			print(ldir)
			os.chdir(ldir)	
			shutil.rmtree("largefile "+filename)#DO SOMETHING ABOUT IT
			print(os.listdir(os.getcwd()))
		if bigdfile==None:#it is a complete file not a part
			File.finallist.update({filename:dfile})	
			folderpagelist[main.curradd].newfile(filename)
		else:#it is a part of some file
			bigdfile.update(dfile)		
	else:
		if isfilesplitted:
			cfold=os.getcwd()		
			b=cfold.rfind('/')		
			ldir=cfold[:b]
			print(ldir)
			os.chdir(ldir)	
			shutil.rmtree("largefile "+filename)#DO SOMETHING ABOUT IT		
			#return None	
	return					



		#join the file	
'''						
def trydistributedupload():
	addfile=main2()
	print("presently i am here"+os.getcwd())
	filesize=int(os.path.getsize(addfile))
	a=addfile.rfind('/')
	filename=addfile[a+1:]
	print(filename)
	totalfreespace=sum(storelist)	
	print("totalfreespace free space="+str(totalfreespace))
	storelist.sort()
	#ssplitsize=splitsize(storelist,filesize)
	ssplitsize=2
	splitfile(addfile,filename,ssplitsize)
	dirlist=os.listdir(os.getcwd())
	print(dirlist)
	##--------MAKE SOMTHING TO DECIDE THE PRIORITY LIST---------------##
	iscorrect=True
	dfile=distributedfile(filename)
	i=0
	for x in dirlist:
		padd=os.getcwd()+'/'+x#partial adress
		psize=int(os.path.getsize(padd))#partial size
		if i<3:
			tmpgdrivefile=gdrivefile(padd)
			tmpgdrivefile.upload()
			print("uploaded file "+str(i)+" "+str(padd)+"google drive")
			gdrivefile.currentquota[1]-=psize
			print("quota updated")
			dfile.update(tmpgdrivefile)
			print("d file updated")
			i=i+1
		elif i<len(dirlist):
			tmpodrivefile=odrivefile(padd)
			tmpodrivefile.upload()
			print("uploaded file"+str(i)+" "+padd+"onedrive")
			odrivefile.currentquota[1]-=psize
			print("quota updated")
			dfile.update(tmpodrivefile)
			print("d file updated")

		elif psize<=dropboxfile.currentquota[1]:
				tmpdropboxfile=dropboxfile(padd)
				tmpdropboxfile.upload()
				dropboxfile.currentquota-=psize
				distributedfile.update(tmpdropboxfile)

			i=i+1
		else:
			print("Sorry the action was unsuccessful.File size could'nt be uploaded.Please free your drive.")
			iscorrect=False
			return None
	cfold=os.getcwd()		
	b=cfold.rfind('/')		
	ldir=cfold[:b]
	os.chdir(ldir)	
	shutil.rmtree("largefile")#DO SOMETHING ABOUT IT
	print(os.listdir(os.getcwd()))		
	return dfile	
'''
	#-------------------------------------3	

					  

#gdrivefile.getquota()
#odrivefile.onedrivequota()
#dropboxfile.quota()

#print(gdrivefile.currentquota)
#print(odrivefile.currentquota)
#print(dropboxfile.currentquota)
#print(dropboxfile.currentquota)  
#a=odrivefile(main2())
#a.upload()

#'''-----------------------------------code for gui tested here---------//

w=page("/Home/")
#imgadd='/home/trueutkarsh/Pictures/downloadfolderfinal.png'


folderpagelist={}
folderpagelist.update({"/Home/":w})


File=FinalList()
File.update()
#File.printaddress()#-TO PRINT FINAL LIST  UNCOMMENT THIS LINE
gdrivefile.currentquota=[1,7*1024*1024]
odrivefile.currentquota=[2,6*1024*1024]
dropboxfile.currentquota=[3,4*1024*1024]
storelist=[odrivefile.currentquota[1],gdrivefile.currentquota[1],dropboxfile.currentquota[1]]#and other drives can be added further dropboxfile.currentquota[1]-removed dropbox

folderpagelist={}
folderpagelist.update({"/Home/":w})

for x,y in File.finallist.items():
	try:
		makebrowser(y.address,folderpagelist,w)
	except:
		print("error in this address"+ y.address)
		
main=Main(folderpagelist,"/Home/")
main.update(folderpagelist,"/Home/")
main.show()
sys.exit(abc.exec_())


#'''


'''---------------CODE FOR GUI ENDS HERE--------------------------------------'''			
  

#testing the new update

#google drive testing takes place here

'''
while True:
	command=raw_input('which propoerty do you want to test for google drive :').strip()
	if command=="download":
		gdrivefile.download()
	elif command=="upload":
		add=raw_input("enter address of a file").strip()
		gdrivefile.upload(add)
	elif command =="updatefilelist":
		gdrivefile.updatefilelist()
		for name in gdrivefile.filelist:
			print name['title']
	elif command=="getquota":
		gdrivefile.getquota()		
		a=gdrivefile.currentquota
		for data in a:
			print(data)+ ' bytes'
	elif command=="exit" :
		break
	else :
		pass	

'''

#odrivefile.authorize()
#os.system("onedrive-cli put Game of Thrones S05E05 1080p HDTV [G2G.fm].srt")

		
#one drive testing 
#odrivefile.authorize()

#odrivefile.getfilelist()
#odrivefile.download()
#odrivefile.updatefilelist()
#odrivefile.download()
#odrivefile.oprintquota()
'''
gdrivefile.authorize()
gdrivefile.updatefilelist()
for x in gdrivefile.filelist:
	add=x['originalFilename']
	print add
'''
'''----FUNCTION TO CHECK DOWNLOAD FROM COMMON DATA BASE.JUST WRITE FILE NAME OF FILE 2 DOWNLOAD FROM ANY OF THE THREE DRIVES'''
'''
a=QApplication(sys.argv)
File=FinalList()
File.update()
#File.printaddress()#-TO PRINT FINAL LIST  UNCOMMENT THIS LINE

w=page("/Home/")
folderpagelist={}
folderpagelist.update({"/Home/":w})
for x,y in File.finallist.items():
	try:
		makebrowser(y.address,folderpagelist,w)
	except:
		print("error in this address"+ y.address)
for x,y in folderpagelist.items():
	y.arrange() 
#folderpagelist["/Home/"].show()				
#folderpagelist["/Home/"].show()
mainwindow=QMainWindow()
scroll=QScrollArea()
scroll.setWidget(folderpagelist["/Home/"])
scroll.setWidgetResizable(True)
scroll.setFixedWidth(800)
layout=QVBoxLayout(folderpagelist["/Home/"])
layout.addWidget(scroll)

mainwindow.setCentralWidget(folderpagelist["/Home/"])
mainwindow.show()
sys.exit(a.exec_())
'''
'''
command='download'
while  command=='download':
	File.download()
	command=raw_input("Enter command").strip()
'''
'''----PRESENTLY UPLOAD IS DRIVE SPECIFIC MAKE AN INSTANCE OF RESPECTIVE DRIVE CLASS AND INITIALIZE IT WITH ITS FILE ADDRESS ON PC'''	



'''
odrivefile.updatefilelist()
odrivefile.printfilelist()
odrivefile.onedrivequota()
print(odrivefile.currentquota)

f1=odrivefile(raw_input('Enter address of file'))
f1.upload()


#odrivefile.printfilelist()
#odrivefile.upload()




os.system("onedrive-cli ls 'Documents/ITSP/'")
<<<<<<< HEAD

=======
'''
'''
gdrivefile.authorize()
dropboxfile.authorize()

odrivefile.authorize()
>>>>>>> origin/master
odrivefile.updatefilelist()
gdrivefile.updatefilelist()
finallist={}
folder=[]
#Code to print file list of dropbox. 
#dropboxfile.printlist("/")
odrivefile.makefinallist(finallist,odrivefile.filelist,folder)
gdrivefile.makefinallist(finallist,gdrivefile.filelist)
dropboxfile.makefilelist(add,finallist)
for a,b in finallist.items():
	print(a,b.address)
filename=''	
while filename!='exit':	
	filename=raw_input("Enter filename(exit to exit)").strip()
	finallist[filename].download()	

gdrivefile.updatefilelist()
for x in gdrivefile.filelist:
	print x['title']

<<<<<<< HEAD
#print(templink)

for line in templink:
	print(line+'we did it')
'''	
	
'''-------------------------WRITE BUGS/'IMPROVEMENT TO BE MADE' HERE-------------------------------------------
1.File name anywhere should not contain "'"	
2.If any change has been made to such as download or upload of a file,filelist should be update there for that file.not complete
update file should be called.
3.There should be folder structures in UI.Files should be shown to be in folders and stuff.
4.Make a last authorized time in each drive classes.So that a user h


-----------------------------------------------------------------------------------'''
#code for getting link of a file in onedrive
'''-----------------------------------------------MAIN PROGRAM AFTERWARDS--------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------------------------------------------------------------------'''
