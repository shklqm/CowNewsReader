from Tkinter import *
from PIL import ImageTk, Image
import ResizeableCanvas, directory
from requests import session
from bs4 import BeautifulSoup

class Login(object):
	def __init__(self,dirObj):
		self.usr		= ""
		self.pwd 		= ""
		self.dirObj		= dirObj
		self.img 		= None
		self.root		= None
		self.mycanvas 	= None
		self.status		= None
		self.mySession	= None
		self.loginText	= None

	def focusEntry(self,event):
		if (event.widget.get() == "username" or event.widget.get() == "password"):
			event.widget.delete(0, END)

		return True

	def addingPassword(self,e):
		if e.get() != "password" and e.get() != "":
			if len(e.get()) > len(self.pwd):
				if len(self.pwd) == 0:
					self.pwd = e.get()
					e.set("*" + e.get()[:-1])
				else:
					flag = False	
					for i in xrange(len(e.get())-1):
						if e.get()[i] != '*' and len(e.get()) != 0:
							self.pwd = self.pwd[:i] + e.get()[i] + self.pwd[i:]
							e.set(e.get()[:i] + '*' +	 e.get()[i+1:])
							flag = True
							break

					if not flag:
						self.pwd += e.get()[len(e.get())-1]
						e.set("*" + e.get()[:-1])
			elif len(e.get()) == 1 and len(self.pwd) == 1:
				self.pwd = e.get()
				e.set('*')
			else:
				self.pwd = self.pwd[:-1]
				e.set("*" + e.get()[:-1])
		else:
			if len(e.get()) == 0 and len(self.pwd) > 0:	
				self.pwd = ""

	def logIn(self,e1):
		self.usr = e1.get()

		payload = {
		    'action': 'login',
		    'username': self.usr,
		    'password': self.pwd
		}

		self.mySession = session()
		self.mySession.post('https://cow.ceng.metu.edu.tr/login.php', data=payload)
		response = self.mySession.get('https://cow.ceng.metu.edu.tr/')

		chunk 	= (response.text)
		soup 	= BeautifulSoup(chunk, 'lxml')
		res 	= soup.find(class_ = "head-menu-left")

		if res == None:
			self.loginFailed()
		elif res.get_text()[:8] == self.usr:
			self.status = 1

		if self.status:
			self.dirObj.saveUserInfo(self.usr, self.pwd)
			self.closeLogInWindow()

	def loadBackground(self,w,h):
		path 		= "/usr/share/cownewsreader/media/login.jpg"
		imag 		= Image.open(path)
		imag 		= imag.resize((w, h), Image.ANTIALIAS)
		self.img 	= ImageTk.PhotoImage(imag)
		return self.img

	def createLogInWindow(self):
		self.root = Tk()
		
		myframe 				= Frame(self.root)
		myframe.pack(fill		= BOTH, expand=YES)
		w, h 					= self.root.winfo_screenwidth(), self.root.winfo_screenheight()
		self.mycanvas 			= ResizeableCanvas.ResizingCanvas(myframe,width=w, height=h, bg="white", highlightthickness=0)
		self.mycanvas.pack(fill	= BOTH, expand=YES)
		self.mycanvas.create_image(w/2,h/2, image=self.loadBackground(w,h))
		
		es2 = StringVar()
		es2.trace("w", lambda name, index, mode, es2=es2: self.addingPassword(es2))
		
		e1 = Entry(self.mycanvas)
		e2 = Entry(self.mycanvas,textvariable=es2)
		self.mycanvas.create_window(w/2, h/2-15,window=e1)
		self.mycanvas.create_window(w/2, h/2+15,window=e2)
		e1.insert(0, "username")
		e2.insert(0, "password")

		e1.bind("<FocusIn>",self.focusEntry)
		e2.bind("<FocusIn>",self.focusEntry)
		
		login_button = Button(self.root, text = "Log In", command = lambda: self.logIn(e1), anchor = 'w', width = 17, activebackground = "#33B5E5")
		login_button_window = self.mycanvas.create_window(w/2-82, h/2+50, anchor='nw', window=login_button)
		login_button.bind("<Return>", lambda event, arg = e1: self.logIn(arg))
		
		# tag all of the drawn widgets
		self.mycanvas.addtag_all("all")
		self.root.mainloop()

	def closeLogInWindow(self):
		self.root.destroy()
		self.status = 1

	def loginFailed(self):
		if self.loginText == None:
			self.loginText = self.mycanvas.create_text(self.root.winfo_screenwidth()/2-85, self.root.winfo_screenheight()/2 + 80, text='Logging in was unsuccessful!', fill = "white", anchor='nw')

