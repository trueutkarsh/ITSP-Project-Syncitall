import httplib2
import pprint
import time
import os
import shutil
#import urllib2
#libraries for gdrive file upload
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
#libraries for onedrive file upload

#libraries for dropbox file upload

class file:#bas class file
	authorized=False#whether authorization has taken place or not
	listupdated=False#whether file list is updated or not
	downloadfilepath=None
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

	def upload(self):
		if gdrivefile.authorized==False :
			gdrivefile.authorize()
			gdrivefile.authorized=True

		FILENAME = self.address
		media_body = MediaFileUpload(FILENAME, mimetype='', resumable=True)
		body = {
		  'title': FILENAME,
		  'description': '',
		  'mimeType': ''
		}
		try:
			file = gdrivefile.drive_service.files().insert(body=body, media_body=media_body).execute()
			#iINSERT CODE TO UPDATE FILE LIST
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
		driver=webdriver.Firefox()#depends on your browser
		driver.get(authorize_url)
		#login=driver.find_element_by_name("signIn")
		#login.send_keys(Keys.RETURN)
		accept= WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "submit_approve_access")))
		accept.send_keys(Keys.RETURN)
    	#accept.click()
		a=driver.find_element_by_id("code")

		code=a.get_attribute('value')
		driver.quit()
		#code = raw_input('Enter verification code: ').strip()#change here
		credentials = flow.step2_exchange(code)

		# Create an httplib2.Http object and authorize it with our credentials
		http = httplib2.Http()
		http = credentials.authorize(http)

		gdrivefile.drive_service = build('drive', 'v2', http=http)
	@staticmethod
	def updatefilelist():#information about files on your drive
		if gdrivefile.authorized==False :
			gdrivefile.authorize()
			gdrivefile.authorized=True
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
	@staticmethod
	def getfile():
		if gdrivefile.listupdated==False:
			gdrivefile.updatefilelist()
		ref=[]	
		sample=raw_input('enter the file name ').strip()
		for gfile in gdrivefile.filelist:
			if sample in gfile['title']:
				if sample==gfile['title']:
					return gfile
				ref.append(gfile['title'])
		print("No match found.Following are the related files")
		for name in ref:
			print(name)	
		return None				



	@staticmethod					
	def download():
		file2download=gdrivefile.getfile()
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
					#src=r"C:\\Users\\windows\\Downloads\\" +  file2download.get('title')
					#dest=os.getcwd()+r"\\" file2download.get('title')
					#shutil.move(dest,src)	

					downloadedfile.close()
					#os.rename(dest,src)
					
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
				
				

  			


			 


				

		

					



		
			  

class odrivefile(file):
	def upload(self):
		#code for upload
		pass

	@staticmethod
	def authorize():
		pass
		#code for authorization	

class drobboxfile(file):
	def upload(self):
		#code for upload
		pass

	@staticmethod
	def authorize():
		pass
		#code for authorization	
#testing the new update
'''	
add=raw_input("enter address of a file")
f1=gdrivefile(add)
f1.upload()
#f1.upload()
'''

#gdrivefile.download()
gdrivefile.getquota()
a=gdrivefile.currentquota
for data in a:
	print(data)+' bytes'

