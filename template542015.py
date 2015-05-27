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
'''
def main1():
	adda=QString()
	adda=QFileDialog.getExistingDirectory()
    return adda
	# main2() gets file name through dialog box.
def main2():
	addb=QString()
	addb=QFileDialog.getOpenFileName()
    return addb	
'''

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
	downloadfilepath='/home/utkarsh/Downloads/Syncitall Goodle drive Downloads'

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
			a=driver.find_element_by_id("code")
                
			code=a.get_attribute('value')		
			driver.quit()
			gdrivefile.authorized=True
		except:
			print "Could not authorize to Google Drive"
			return None
#3>>>>>>> origin/master
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
					
	def download(self):
		if gdrivefile.listupdated==False:
			gdrivefile.updatefilelist()
		gdrivefile.listupdated=True	
		for a in gdrivefile.filelist:
			if a['title']==self.address:
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
					add2=main1()
					src=add2+"/"+ file2download.get('title')
					dest=os.getcwd()+"/"+ file2download.get('title')
#>>>>>>> origin/master
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
		gdrivefile.currentquota=[about['quotaBytesTotal'],about['quotaBytesUsed']]
	@staticmethod
	def makefinallist(finallist,filelist):

		for name in filelist:
			tmpgdrivefile=gdrivefile(name['title'])
			finallist.update({str(name['title']):tmpgdrivefile})
		
				
				

  			

class odrivefile(file):
	filelist=None
	currentquota=None
	downloadfilepath='/home/utkarsh/Downloads/Syncitall Onedrive Downloads'
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
		odrivefile.currentquota=commands.getstatusoutput('onedrive-cli quota')[1].strip()	

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
	def download(self):
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
		tempcontent=commands.getstatusoutput("onedrive-cli get '"+ofile2download+"'")
		downloadedfile.write(tempcontent[1])
		src=os.getcwd()+'/'+filename
		d=main1()
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
	def upload(self):
		
		if dropboxfile.authorized==False :
			dropboxfile.authorize()
			dropboxfile.authorized=True
		#code for upload
		
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
			code=driver.find_element_by_id("auth-code").get_attribute("innerHTML")
                
				
			driver.quit()
			dropboxfile.authorized=True
		except:
			print "Could not authorize to dropbox"
			return None
		dropbox.access_token, dropbox.user_id = flow.finish(code)
		dropboxfile.client = dropbox.client.DropboxClient(dropbox.access_token)
		dropboxfile.account=dropboxfile.client.account_info()
		#code for authorization	
	
	def download(self):
		if dropboxfile.authorized==False :
			return None
		try:		
			f, metadata = dropboxfile.client.get_file_and_metadata(self.address)
		except TypeError:
			file.found=0
		add=main1()
		
		out = open(add+"/"+ntpath.basename(self.address), 'wb')
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
		dropboxfile.makefilelist(add,self.finallist)
		folder=[]
		odrivefile.makefinallist(self.finallist,odrivefile.filelist,folder)
		gdrivefile.makefinallist(self.finallist,gdrivefile.filelist)
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
        #
        self.name=name
        self.foldername.setText(name)
        self.foldername.move(self.x()+self.width(),self.y()+self.pic.height()/2-10)#move text to appropriate height
        self.mousePressEvent = self.gotclickedevent
        self.foldername.mousePressEvent=self.gotclickedevent
        self.mouseDoubleClickEvent = self.gotclickedevent
        self.foldername.mouseDoubleClickEvent=self.gotclickedevent
        self.pageadd=page.windowtitle
        #self.installEventFilter(self)
        self.h=QVBoxLayout()
        
        
        self.txtlabel=QLabel()
        self.txtlabel.setToolTip(name)

        #txtlabel.setFixedSize(130,10)
        #txtlabel.setStyleSheet("QWidget {background-color:blue}")
        if len(name)>15:
            name=name[:11]+"..."
        self.txtlabel.setText(name)
        self.txtlabel.setFixedSize(130,20)
        self.txtlabel.setAlignment(Qt.AlignCenter)
        self.setAlignment(Qt.AlignCenter)
        
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
        main.update(folderpagelist,self.pageadd+self.name+"/")
        
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
        main.update(folderpagelist,self.pageadd+self.name+"/")
        main.show()
        main.curradd=self.pageadd+self.name+"/" 
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
            icon.h.addWidget(icon.txtlabel)   
            overall.addWidget(icon)
            overall.addWidget(icon.txtlabel)

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
        newfolder=QAction('New Folder',self)
        self.menu.addAction(paste)
        self.menu.addAction(newfolder)
        #Download.triggered.connect(lambda x:File.download(self.name))
        #cut.triggered.connect(lambda x:folderpagelist[main.curradd].cut(self))#change here
        paste.triggered.connect(lambda x:folderpagelist[main.curradd].paste())
        self.menu.popup(QCursor.pos())


    	                  
  
#class fileicon()
#add=main2()
#a=odrivefile(add)
#a.upload()
w=page("/Home/")
#imgadd='/home/trueutkarsh/Pictures/downloadfolderfinal.png'


folderpagelist={}
folderpagelist.update({"/Home/":w})


File=FinalList()
File.update()
#File.printaddress()#-TO PRINT FINAL LIST  UNCOMMENT THIS LINE


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
