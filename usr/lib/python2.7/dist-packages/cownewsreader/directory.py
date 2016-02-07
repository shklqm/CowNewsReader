import os,sys
import base64

class Directory(object):
	def startDir(self):
		if not os.path.isdir(os.path.expanduser('~') + "/.CowNewsReader"):
			if os.system("mkdir " + os.path.expanduser('~') + "/.CowNewsReader"):
				print "Error: Couldn't create directory"
				sys.exit(1)
		
		if not os.path.isdir(os.path.expanduser('~') + "/.CowNewsReader/images"):
			if os.system("mkdir " + os.path.expanduser('~') + "/.CowNewsReader/images"):
				print "Error: Couldn't create directory"
				sys.exit(1)

		if not os.path.isfile(os.path.expanduser('~') + "/.CowNewsReader/pref.txt"):
			os.system("touch " + os.path.expanduser('~') + "/.CowNewsReader/pref.txt")

		if not os.path.isfile(os.path.expanduser('~') + "/.CowNewsReader/pwd.txt"):
			os.system("touch " + os.path.expanduser('~') + "/.CowNewsReader/pwd.txt")

	def saveUserInfo(self, name, pwd):
		try:
		    f 	= open(os.path.expanduser('~') + "/.CowNewsReader/pwd.txt", 'w')
		    nm 	= f.softspace
		except IOError, e:
		    print e
		    sys.exit(0)

		enName 	= base64.b64encode(name[1:])
		enPwd	= base64.b64encode(pwd)    
		pd 		= int(base64.b64decode(enName))%10

		for i in xrange(nm):
			enName = base64.b64encode(enName)

		for i in xrange(pd):
			enPwd = base64.b64encode(enPwd)

		f.write(enName+"\n")
		f.write(enPwd)

		f.close()

	def readUserInfo(self):
		try:
		    f 	= open(os.path.expanduser('~') + "/.CowNewsReader/pwd.txt", 'r')
		except IOError, e:
		    print e
		    sys.exit(0)

		nro		= base64.b64decode(f.readline().strip("\n"))
		pso		= base64.b64decode(f.readline().strip("\n"))

		for i in xrange(int(nro)%10):
			pso = base64.b64decode(pso)
