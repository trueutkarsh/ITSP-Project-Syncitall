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
import pickle
import sys
from PyQt4.QtGui import  *
from PyQt4.QtCore import *
saved_list={}
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
class account:
	gname=''
	gpass=''
	oname=''
	opass=''
	dname=''
	dpass=''
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
	tobeauthorized=False
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
		try:
			flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
						   redirect_uri=REDIRECT_URI)
			authorize_url = flow.step1_get_authorize_url()
		except:
			print "No internet connection"
			return
		#print 'Go to the following link in your browser: ' + authorize_url

		try:		
			driver=webdriver.PhantomJS()#depends on your browser
			driver.get(authorize_url)
			WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "Email"))).send_keys(account.gname)
			WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "Passwd"))).send_keys(account.gpass)	
			WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "signIn"))).click()		
			WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "submit_approve_access"))).click()
			code1= WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "code")))
			code=code1.get_attribute('value')		
			driver.quit()
			gdrivefile.authorized=True
			print "Google drive authorized"
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
	tobeauthorized=False
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
			driver=webdriver.PhantomJS()
			authurl= 'https://login.live.com/oauth20_authorize.srf?scope='+oscope+'&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf&response_type=code&client_id=000000004015642C'
			driver.get(authurl)
			WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "i0116"))).send_keys(account.oname)
			WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "i0118"))).send_keys(account.opass)
			WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()

			WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "idBtn_Accept"))).click()
			endurl=str(driver.current_url)
			driver.quit()
			os.system("onedrive-cli auth "+ endurl)
			odrivefile.authorized=True
			print "Onedrive authorized"
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
				foldername=''
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
	tobeauthorized=False
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
		try:
			flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
			authorize_url = flow.start()
		except:
			print "No internet connection"
			return
		try:
			driver=webdriver.PhantomJS()#depends on your browser
			driver.get(authorize_url)
			driver.save_screenshot('screen1.png')
			(WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="text-input-input autofocus"]')))).send_keys(account.dname)
			(WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="password-input text-input-input"]')))).send_keys(account.dpass)
			driver.save_screenshot('screen2.png')
			(WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))).click()
			(WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.NAME, "allow_access")))).click()
			driver.save_screenshot('screen5.png')
			code1= WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "auth-code")))
			code=code1.get_attribute("innerHTML")
			driver.quit()
			dropboxfile.authorized=True
			print "Dropbox authorized"
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
				'''
		for x in folder_metadata['contents']:
			if x['is_dir']==False:
				print "I was here"
				if ntpath.basename(x['path'])=="mouse.sh":
					print "I was here too"
					dropboxfile.client.file_delete(x['path'])
					print x['path']
					rev= dropboxfile.client.revisions(x['path'],rev_limit=2)
					print rev[0]
					dropboxfile.client.restore(x['path'],rev[0])
				'''
	@staticmethod
	def quota():
		if dropboxfile.authorized==None:
			print "Dropbox not authorized"
			return None
		else:
			print ("shared : " +str(dropboxfile.account['quota_info']['shared']))
			print ("quota  : " +str(dropboxfile.account['quota_info']['quota']))
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
		if gdrivefile.tobeauthorized==True:
			if True:
				gdrivefile.authorize()
				gdrivefile.updatefilelist()
				gdrivefile.makefinallist(self.finallist,gdrivefile.filelist)
			else:
				print "Could not make filelist"
		if dropboxfile.tobeauthorized==True:
			try:
				dropboxfile.authorize()
				add='/'
				dropboxfile.makefilelist(add,self.finallist)
			except:
				print "Could not make filelist"
		if odrivefile.tobeauthorized==True:
			try:
				odrivefile.authorize()
				odrivefile.updatefilelist()
				folder=[]
				odrivefile.makefinallist(self.finallist,odrivefile.filelist,folder)
			except:
				print "Could not make filelist"
	def printaddress(self):
		for a,b in self.finallist.items():
			print(a,str(b.address))#change here
	def download(self,filename):
		#filename=raw_input("Name of file").strip()
		self.finallist[filename].download()		
'''--------------------CODE FOR GUI STARTS HERE---------------------------'''					
main=None
abc=QApplication(sys.argv)


#This code is to get any new icons or directories created in cloud storage.
	
def process_list():
	for a,b in folderpagelist.items():
		for c in b.iconlist:
			if b.windowtitle+c.name not in saved_list.keys():
				saved_list.update({b.windowtitle+c.name:None})
	pickle.dump(saved_list,open('workfile.pkl','wb'))
#This function is to change the folderpagelist according to data saved 
#in saved_list.	
def process_folderpagelist():
	#Make all new folders
	for i in saved_list.keys():
		if i[-1]=="/":
			tmppage=page(i)
			folderpagelist.update({i:tmppage})
	#Assign icons to new folders.
	for i in saved_list.keys():
		if i[-1]=="/":
			j=i[:-2].rfind("/")
			name=i[j+1:-1]
			rname=i[:j]+"/"
			if rname in folderpagelist.keys():
				icon=foldericon(folderpagelist[rname],name)
				folderpagelist[rname].iconlist.append(icon)

	#Take care of moved icons.
	for a,b in saved_list.items():
		if b!=None:
			if b=="*trashed#":
				i=a.rfind("/")
				srcname=a[i+1:]
				srcdirname=a[:i+1]
				if srcdirname in folderpagelist.keys():
					for k in folderpagelist[srcdirname].iconlist:
						if k.name==srcname:
							folderpagelist[srcdirname].iconlist.remove(k)
							trash.iconlist.append(k)
			elif b== "*trashedf#" :
				i=a.rfind("/")
				srcname=a[i+1:]
				srcdirname=a[:i+1]				
				if srcdirname in folderpagelist.keys():
					for k in folderpagelist[srcdirname].iconlist:
						if k.name==srcname:
							folderpagelist[srcdirname].iconlist.remove(k)
							trash.iconlist.append(k)
							trash.page_list.append(folderpagelist[a+"/"])
							del folderpagelist[a+"/"]
			else:
				i=a.rfind("/")
				srcname=a[i+1:]
				srcdirname=a[:i+1]
				j=b.rfind("/")
				dstdirname=b[:j+1]
				if srcdirname in folderpagelist.keys():
					if dstdirname in folderpagelist.keys():			
						for k in folderpagelist[srcdirname].iconlist:
							if k.name==srcname:
								folderpagelist[dstdirname].iconlist.append(k)
								folderpagelist[srcdirname].iconlist.remove(k)
	

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
				for a in main.movelist:
					saved_list.update({a.ad+a.name:self.address+a.name})
			#main.update(folderpagelist,self.address)
				yo(folderpagelist,self.address)#modifies the page..
				del main.movelist[:] 
		pickle.dump(saved_list,open('workfile.pkl','wb'))

	def delete(self,icon):
		trash.iconlist.append(icon)
		self.iconlist.remove(icon)
		saved_list.update({icon.ad+icon.name:"*trashed#"})
		pickle.dump(saved_list,open('workfile.pkl','wb'))
		yo(folderpagelist,self.windowtitle)
	def deletef(self,icon):
		trash.iconlist.append(icon)
		self.iconlist.remove(icon)
		for k in folderpagelist.keys():
			if k==icon.ad+icon.name+"/":
				trash.page_list.append(folderpagelist[k])
				del folderpagelist[k]
		saved_list.update({icon.ad+icon.name:"*trashedf#"})
		pickle.dump(saved_list,open('workfile.pkl','wb'))		
		yo(folderpagelist,self.windowtitle)

def yo(folderpagelist,address):
	main.clear(main.mainLayout)
	main.update(folderpagelist,address)
	main.show()
class Trash(page):
	def __init__(self,add):
		super(Trash,self).__init__(add)
		self.page_list=[]
	def restore(self,icon):
		if icon.ad in folderpagelist.keys():
			folderpagelist[icon.ad].iconlist.append(icon)
			trash.iconlist.remove(icon)
			del saved_list[icon.ad+icon.name]
			pickle.dump(saved_list,open('workfile.pkl','wb'))			
			yo(folderpagelist,"/Trash/")
	def restoref(self,icon):
		if icon.ad in folderpagelist.keys():
			for b in self.page_list:
				if b.windowtitle==icon.ad+icon.name+"/":
					folderpagelist.update({icon.ad+icon.name+"/":b})
			self.iconlist.remove(icon)
			del saved_list[icon.ad+icon.name]
			folderpagelist[icon.ad].iconlist.append(icon)
			pickle.dump(saved_list,open('workfile.pkl','wb'))			
			yo(folderpagelist,"/Trash/")
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
		nname=name
		if len(name)>15:
			nname=name[:11]+"..."
		self.txtlabel.setText(nname)
		self.txtlabel.setFixedSize(130,20)
		self.txtlabel.setAlignment(Qt.AlignCenter)
		self.setAlignment(Qt.AlignCenter)
	def new_fol(self):
		self.new_label.hide()
		txt=self.new_label.text()
		self.name=str(txt)
		self.txtlabel.setText(self.name)
		new_page=page(self.page.windowtitle+self.name+"/")
		saved_list.update({self.page.windowtitle+self.name+"/":None})
		pickle.dump(saved_list,open('workfile.pkl','wb'))
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
		super(foldericon,self).__init__(page,name,'folder.png')
	def gotclickedevent(self,event):
		super(foldericon,self).gotclickedevent(event)
	def doubleclickevent(self):
		
		main.clear(main.mainLayout)
		#main.mainLayout.removeWidget(main.backbutton)
		#main.mainLayout.removeWidget(main.scroll)
		main.update(folderpagelist,self.ad+self.name+"/")
		main.show()
		main.curradd=self.ad+self.name+"/" 
	def contextMenuEvent(self, event):
		#index = self.indexAt(event.pos())
		self.menu = QMenu()
		delete=QAction('Delete',self)
		self.menu.addAction(delete)
		delete.triggered.connect(lambda x:folderpagelist[main.curradd].deletef(self))
		restore=QAction('Restore',self)
		self.menu.addAction(restore)
		restore.triggered.connect(lambda x:trash.restoref(self))
		self.menu.popup(QCursor.pos())

	#define leftclickevent,rightclickevent,doubleclickevent

class fileicon(icon):
	def __init__(self,page,name):
		super(fileicon,self).__init__(page,name,'file.png') 
	def contextMenuEvent(self, event):
		#index = self.indexAt(event.pos())
		self.menu = QMenu()
		renameAction = QAction('Exit',self)
		Download = QAction('Download',self)
		delete=QAction('Delete',self)
		cut=QAction('Cut',self)
		paste=QAction('Paste',self)
		self.menu.addAction(paste)
		self.menu.addAction(Download)
		self.menu.addAction(cut)
		self.menu.addAction(delete)
		restore=QAction('Restore',self)
		self.menu.addAction(restore)
		restore.triggered.connect(lambda x:trash.restore(self))
		Download.triggered.connect(lambda x:File.download(self.name))
		cut.triggered.connect(lambda x:folderpagelist[main.curradd].cut(self))#change here
		paste.triggered.connect(lambda x:main.paste())
		delete.triggered.connect(lambda x:folderpagelist[main.curradd].delete(self))
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
			#self.mainHLayout=QHBoxLayout()
			#self.mainVLayout=QVBoxLayout()
			self.mainLayout=QGridLayout()
			self.container=QWidget()
			self.scroll=QScrollArea()
			self.layout=QGridLayout()
			self.backicon=QIcon()
			self.home=QIcon()
			self.trash=QIcon()
			self.curradd=address
			self.movelist=[]
			a=QSize(90,90)
			self.backicon.addFile('back.png',a,QIcon.Normal,QIcon.On)
			self.home.addFile('home.png',a,QIcon.Normal,QIcon.On)
			self.trash.addFile('trash.png',a,QIcon.Normal,QIcon.On)
	def update(self,folderpagelist,address):
		self.hlayout=QHBoxLayout()
		self.layout=QGridLayout()
		self.container=QWidget()
		self.scroll=QScrollArea()
		self.layout=QGridLayout()
		self.backbutton=QPushButton(self.backicon,"Back",self.centralWidget)
		self.homebutton=QPushButton(self.home,"Home",self.centralWidget)
		self.trashbutton=QPushButton(self.trash,"Trash",self.centralWidget)
		self.backbutton.setFixedSize(60,24)
		self.homebutton.setFixedSize(60,24)
		self.trashbutton.setFixedSize(60,24)
		self.backbutton.clicked.connect(self.lp)
		self.homebutton.clicked.connect(self.homef)
		self.trashbutton.clicked.connect(self.trashf)
		#self.mainVLayout.addWidget(self.homebutton)
		#self.mainVLayout.addWidget(self.trashbutton)
		###
		folderpagelist[address].setLayout(self.layout)
		self.ad=address
		k=0
		j=0
		i=0
		self.positions=[] 
		while(i<len(folderpagelist[address].iconlist)):
			j=0
			while(j<4 and i<len(folderpagelist[address].iconlist )):
					
				self.positions=self.positions+[(k,j)]
				j=j+1
				i=i+1
			k=k+1
			
			#pos1=QMouseEvent.pos()
			#m=QMouseEvent()
			
		for position,icon in zip(self.positions,folderpagelist[address].iconlist):
				
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
		self.mainLayout.addWidget(self.homebutton)
		self.mainLayout.addWidget(self.trashbutton)
		self.mainLayout.addWidget(self.backbutton)
		self.mainLayout.addWidget(self.scroll)
		#self.mainHLayout.addItem(self.mainLayout)
		#self.mainHLayout.addItem(self.mainVLayout)
		self.centralWidget.setLayout(self.mainLayout)	
		#self.centralWidget.setMaximumSize(600,600)
	def homef(self):
		yo(folderpagelist,"/Home/")
	def trashf(self):
		yo(folderpagelist,"/Trash/")
	def lp(self):
		count=self.ad[:-1].count('/')
		if count>1:
			i=self.ad[:-1].rfind("/")
			yo(folderpagelist,self.ad[:i+1])
			self.curradd=self.ad[:i+1]
			print("curr add is" +self.curradd)
		else:
			print("You are in base directory")	
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
		print self.ad
		new.triggered.connect(folderpagelist[self.ad].newfolder)
		self.menu.addAction(new)		
		#Download.triggered.connect(lambda x:File.download(self.name))
		#cut.triggered.connect(lambda x:folderpagelist[main.curradd].cut(self))#change here
		paste.triggered.connect(lambda x:folderpagelist[main.curradd].paste())
		self.menu.popup(QCursor.pos())
File=FinalList()
show_token=False
splash=None
main2=None
status=None
w=page("/Home/")
trash=Trash("/Trash/")
#imgadd='/home/trueutkarsh/Pictures/downloadfolderfinal.png'


folderpagelist={}
folderpagelist.update({"/Home/":w})


#stray list is to ensure that workfile.pkl is present to load.
stray_list={'address':None}
#saved list is where all cut-paste data will remain persistent.
try:
	saved_list=pickle.load(open('workfile.pkl','rb'))
except:
	pickle.dump(stray_list,open('workfile.pkl','wb'))
	saved_list=pickle.load(open('workfile.pkl','rb'))	

class Welcome(QMainWindow):
	def __init__(self,parent=None):
		super(Welcome, self).__init__(parent)
		self.centralwidget=QWidget()
		self.centralwidget.setFixedSize(250,300)
		self.layout=QVBoxLayout()
		Question=QLabel()
		Question.setText("What do you want to sync?")
		self.layout.addWidget(Question)
		gcb=QCheckBox('Google Drive')
		self.layout.addWidget(gcb)
		gh=QHBoxLayout()
		gh.addStretch(1)
		gv=QVBoxLayout()
		gu=QHBoxLayout()
		gp=QHBoxLayout()
		usrname=QLabel()
		usrname.setFixedSize(70,10)
		usrname.setText("Username")
		passw=QLabel()
		passw.setFixedSize(70,10)
		passw.setText("Password")
		self.ul=QLineEdit()
		self.ul.setEnabled(False)
		self.pl=QLineEdit()
		self.pl.setEnabled(False)
		gu.addWidget(usrname)
		gu.addWidget(self.ul)
		gp.addWidget(passw)
		gp.addWidget(self.pl)
		gv.addItem(gu)
		gv.addItem(gp)
		gh.addItem(gv)
		gh.addStretch(40)
		self.layout.addItem(gh)
		gcb.stateChanged.connect(self.gfunc)
		dcb=QCheckBox('Dropbox')
		self.layout.addWidget(dcb)		
		dh=QHBoxLayout()
		dh.addStretch(1)
		dv=QVBoxLayout()
		du=QHBoxLayout()
		dp=QHBoxLayout()
		usrname=QLabel()
		usrname.setFixedSize(70,10)
		usrname.setText("Username")
		passw=QLabel()
		passw.setFixedSize(70,10)
		passw.setText("Password")
		self.dul=QLineEdit()
		self.dul.setEnabled(False)
		self.dpl=QLineEdit()
		self.dpl.setEnabled(False)
		du.addWidget(usrname)
		du.addWidget(self.dul)
		dp.addWidget(passw)
		dp.addWidget(self.dpl)
		dv.addItem(du)
		dv.addItem(dp)
		dh.addItem(dv)
		dh.addStretch(40)
		self.layout.addItem(dh)
		dcb.stateChanged.connect(self.dfunc)
		ocb=QCheckBox('Onedrive')
		self.layout.addWidget(ocb)		
		oh=QHBoxLayout()
		oh.addStretch(1)
		ov=QVBoxLayout()
		ou=QHBoxLayout()
		op=QHBoxLayout()
		usrname=QLabel()
		usrname.setFixedSize(70,10)
		usrname.setText("Username")
		passw=QLabel()
		passw.setFixedSize(70,10)
		passw.setText("Password")
		self.oul=QLineEdit()
		self.oul.setEnabled(False)
		self.opl=QLineEdit()
		self.opl.setEnabled(False)
		ou.addWidget(usrname)
		ou.addWidget(self.oul)
		op.addWidget(passw)
		op.addWidget(self.opl)
		ov.addItem(ou)
		ov.addItem(op)
		oh.addItem(ov)
		oh.addStretch(40)
		self.layout.addItem(oh)
		ocb.stateChanged.connect(self.ofunc)
		self.button=QPushButton()
		self.button.setText("Done")
		self.button.clicked.connect(self.insert)
		self.layout.addWidget(self.button)
		self.centralwidget.setLayout(self.layout)
		self.setCentralWidget(self.centralwidget)
	def insert(self):
		account.gname=str(self.ul.text()).strip()
		account.gpass=str(self.pl.text()).strip()
		account.dname=str(self.dul.text()).strip()
		account.dpass=str(self.dpl.text()).strip()
		account.oname=str(self.oul.text()).strip()
		account.opass=str(self.opl.text()).strip()
		if account.gname!='':
			gdrivefile.tobeauthorized=True
		if account.oname!='':
			odrivefile.tobeauthorized=True
		if account.dname!='':
			dropboxfile.tobeauthorized=True
		File.update()
		if dropboxfile.authorized==True or gdrivefile.authorized==True or odrivefile.authorized==True:
			self.hide()
			for x,y in File.finallist.items():
				try:
					makebrowser(y.address,folderpagelist,w)
				except:
					print("error in this address"+ y.address)
			process_list()
			process_folderpagelist()
			folderpagelist.update({"/Trash/":trash})
			global main
			main.update(folderpagelist,"/Home/")

			main.show()


	def gfunc(self,state):
		if state==Qt.Checked:
			self.ul.setEnabled(True)
			self.pl.setEnabled(True)
		else:
			self.ul.setEnabled(False)
			self.pl.setEnabled(False)
			self.ul.setText('')
			self.pl.setText('')			
	def dfunc(self,state):
		if state==Qt.Checked:
			self.dul.setEnabled(True)
			self.dpl.setEnabled(True)
		else:
			self.dul.setEnabled(False)
			self.dpl.setEnabled(False)
			self.dul.setText('')
			self.dpl.setText('')	
	def ofunc(self,state):
		if state==Qt.Checked:
			self.oul.setEnabled(True)
			self.opl.setEnabled(True)
		else:
			self.oul.setEnabled(False)
			self.opl.setEnabled(False)
			self.oul.setText('')
			self.opl.setText('')
		'''				  
class start_screen(QLabel):
	def __init__(self,parent=None):
		pic=QPixmap("syncitall.png")
		self.setPixmap(pic)
		'''



#class fileicon()
#add=main2()
#a=odrivefile(add)
#a.upload()
# Simulate something that takes time
main2=Welcome()
#splash.finish(main2)
main=Main(folderpagelist,"/Home/")
main2.show()

status=abc.exec_()
#File.printaddress()#-TO PRINT FINAL LIST  UNCOMMENT THIS LINE












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
