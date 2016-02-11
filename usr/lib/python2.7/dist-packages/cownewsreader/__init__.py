import os,sys
from requests import session
from bs4 import BeautifulSoup
import directory, LogIn

def main():
	obj = directory.Directory()
	obj.startDir()

	#register empty session
	mainSession = None

	payload = {
	    'action': 'login',
	    'username': '',
	    'password': ''
	}

	#Logged in flag
	loggedIn = False

	#check if correctly signed in before
	if os.stat(os.path.expanduser('~') + "/.CowNewsReader/pwd.txt").st_size != 0:	
		f = open(os.path.expanduser('~') + "/.CowNewsReader/pwd.txt")
		usr,pwd = obj.readUserInfo()
		payload['username'] = usr
		payload['password'] = pwd 

		mainSession = session()
		mainSession.post('https://cow.ceng.metu.edu.tr/login.php', data=payload)
		response 	= mainSession.get('https://cow.ceng.metu.edu.tr/')

		chunk 	= (response.text)
		soup 	= BeautifulSoup(chunk, 'lxml')
		res 	= soup.find(class_ = "head-menu-left")

		if res != None and res.get_text()[:8] == usr:
			print "W: Already loggedIn"
			loggedIn = True

	#else bring up the login window
	else: 

		lg = LogIn.Login(obj)	
		lg.createLogInWindow()

		#still unlogged
		if not lg.status :
			print "Error: Couldn't log in"
			sys.exit(1)

		mainSession = lg.mySession
	
	#User is now logged in
