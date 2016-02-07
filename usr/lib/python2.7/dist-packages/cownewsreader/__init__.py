import directory, LogIn

def main():
	obj = directory.Directory()
	obj.startDir()
	lg = LogIn.Login()	
	lg.createLogInWindow()

	print lg.status

