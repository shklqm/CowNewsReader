# -*- coding: utf-8 -*- 
from Tkinter import *
import Image, ImageTk
from random import randint
from bs4 import BeautifulSoup
import threading
import Queue
import os
import json
import time
import urllib


lastNewsPosition 	= 0
allCourses = ["course.100","course.111","course.140","course.213","course.223","course.232","course.242","course.272","course.280","course.301","course.302","course.305","course.315","course.316","course.331","course.332","course.334","course.336","course.340","course.350","course.351","course.352","course.356","course.371","course.372","course.373","course.378","course.380","course.382","course.384","course.424","course.435","course.436","course.437","course.441","course.443","course.444","course.451","course.462","course.463","course.465","course.466","course.469","course.477","course.478","course.482","course.483","course.490","course.493","course.494","course.495","course.497","course.498","course.499","course.508","course.514","course.520","course.530","course.531","course.532","course.536","course.538","course.539","course.540","course.546","course.550","course.551","course.553","course.556","course.559","course.561","course.562","course.563","course.564","course.565","course.566","course.567","course.568","course.569","course.571","course.574","course.577","course.580","course.581","course.583","course.584","course.591","course.701","course.710","course.712","course.713","course.714","course.729","course.732","course.734","course.740","course.769","course.770","course.771","course.773","course.776","course.779","course.784","course.785","course.786","course.778","course.ee281","test","news"]

class NewsReader(object):
	def __init__(self, sourceMessage, imgPath, subjectMessage, fromMessage, dateMessage, messageBody):
		self.canvas 			= None
		self.sourceMessage		= sourceMessage
		self.img 				= None
		self.imgPath 			= imgPath		
		self.subjectMessage 	= subjectMessage
		self.fromMessage 	 	= fromMessage
		self.dateMessage 	 	= dateMessage
		self.messageBody 		= messageBody

	def setCanvas(self, _canvas):
		self.canvas = _canvas

	def createNews(self):
		global lastNewsPosition
		#GET PICTURE
		self.getPicture(self.imgPath)
		self.canvas.create_image(0, lastNewsPosition+10, image = self.img, anchor="nw")

		#GET SUBJECT MESSAGE
		subjectMessageLabel = Label(self.canvas, text="Subject:	" + self.subjectMessage,anchor='w', font="monosa 11 bold",bg='#ABCDEF')
		subjectMessageLabel.pack()
		self.canvas.create_window(120, lastNewsPosition+20, window=subjectMessageLabel, anchor='w')

		#GET FROM MESSAGE
		fromMessageLabel = Label(self.canvas, text="From:	" + self.fromMessage,anchor='w', font="monosa 11 bold",bg='#ABCDEF')
		fromMessageLabel.pack()
		self.canvas.create_window(120, lastNewsPosition+45, window=fromMessageLabel, anchor='w')

		#GET DATE MESSAGE
		dateMessageLabel = Label(self.canvas, text="Date:	"+self.dateMessage,anchor='w', font="monosa 11 bold",bg='#ABCDEF')
		dateMessageLabel.pack()
		self.canvas.create_window(120, lastNewsPosition+70, window=dateMessageLabel, anchor='w')

		#GET SOURCE INFO
		dateMessageLabel = Label(self.canvas, text="Source:	"+self.sourceMessage,anchor='w', font="monosa 11 bold",bg='#ABCDEF')
		dateMessageLabel.pack()
		self.canvas.create_window(120, lastNewsPosition+95, window=dateMessageLabel, anchor='w')

		# GET MESSAGE BODY
		messageBodyLabel = Label(self.canvas, text=self.messageBody,anchor='w', wraplength=self.canvas.winfo_screenwidth(), font="monosa",bg='#ABCDEF')
		messageBodyLabel.pack()
		self.canvas.create_window(0, lastNewsPosition+135+messageBodyLabel.winfo_reqheight()/2, window=messageBodyLabel, anchor='w')

		#update lastNewsPosition
		lastNewsPosition += messageBodyLabel.winfo_reqheight() + 150

		#DRAW THE LINE SEPARATOR
		self.getLineSeparator()
		self.canvas.create_line(0, lastNewsPosition, self.canvas.winfo_screenwidth(), lastNewsPosition, fill="blue", width=3,activefill="brown")

		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def getPicture(self, imgPath):
		File 		= imgPath
		image 		= Image.open(File)
		image 		= image.resize((100, 100), Image.ANTIALIAS)
		self.img 	= ImageTk.PhotoImage(image)

	def getLineSeparator(self):
		self.linePosition = 150

class Response(object):
	def __init__(self,newsId, courseName, responseImg, responseSubjectMessage,responseFromName,responseFromMessage,responseDateMessage,responseMessageBody):
		self.newsId 					= newsId
		self.courseName 				= courseName
		self.responseImg				= responseImg
		self.responseSubjectMessage 	= responseSubjectMessage
		self.responseFromName 	 	 	= responseFromName
		self.responseFromMessage 	 	= responseFromMessage
		self.responseDateMessage 	 	= responseDateMessage
		self.responseMessageBody 		= responseMessageBody

class Request(object):
	def __init__(self, courseName, courseNews, mwSession):
		self.courseName = courseName
		self.courseNews = courseNews
		self.mwSession 	= mwSession
		
class CheckNews(threading.Thread):
    def __init__(self, in_queue, out_queue):
        threading.Thread.__init__(self)
        self.in_queue 	= in_queue
        self.out_queue 	= out_queue

    def extractId(self, inputString):
		nr = ''
		for i in xrange(len(inputString)):
			if inputString[i] == '#':
				nr = inputString[i+1:]
				break;

		return nr

    def run(self):
		req = self.in_queue.get(0)
		# print "thread running..."
		
		try:
			response 	= req.mwSession.get('https://cow.ceng.metu.edu.tr/News/thread.php?group=metu.ceng.' + req.courseName)
		except Exception, e:
			print e
			sys.exit(1)

		chunk 	= (response.text)
		soup 	= BeautifulSoup(chunk, 'lxml')

		rows = soup.findAll('tr', {'class': re.compile("np_thread_line*")})

		newNewsToBeOpened = []
		for _row in rows:
			r1 = _row.find(attrs={"color": "red"})
			r2 = _row.find(href=re.compile("article.php"))
			if r1:
				link 	= r2['href']
				newsId	= self.extractId(link)
				tempList= [link, newsId]
				if not newsId in req.courseNews:
					newNewsToBeOpened.append(tuple(tempList))
					# print "Not there!!"

		newsToBeReturned = []
		#Open each new news
		for i in xrange(len(newNewsToBeOpened)):
			try:
				new_response 	= req.mwSession.get('https://cow.ceng.metu.edu.tr/News/' + newNewsToBeOpened[i][0])
			except Exception, e:
				print e
				sys.exit(1)

			chunk 	= (new_response.text)
			soup 	= BeautifulSoup(chunk, 'lxml')

			title 		= soup.find('div', {'class': 'np_article_header'}).b.next_sibling.strip()
			name 		= soup.find('div', {'class': 'np_article_header'}).a.text.strip()
			date 		= soup.find('div', {'class': 'np_article_header'}).a.next_sibling.next_sibling.next_sibling.next_sibling.strip()
			body 		= soup.find('div', {'class': 'np_article_body'}).text.strip()
			img 		= soup.find(href=re.compile('download_userPicture'))['href'].strip()

			#Check whether the image already exists
			if not os.path.isfile(os.path.expanduser('~') + "/.CowNewsReader/images/" + img[img.find('username=')+9:]):
				urllib.urlretrieve(img, os.path.expanduser('~') + "/.CowNewsReader/images/" + img[img.find('username=')+9:])

			finalImgSrc = os.path.expanduser('~') + "/.CowNewsReader/images/" + img[img.find('username=')+9:]	
			
			#Create response news objects
			newsResponse = Response(newNewsToBeOpened[i][1],req.courseName,finalImgSrc,title,name,name,date,body)
			newsToBeReturned.append(newsResponse)


		if not len(newsToBeReturned):
			#insert just the course name to the output queue
			self.out_queue.put(req.courseName)
		else:	
			#insert newsToBeReturned to the output queue
			self.out_queue.put(newsToBeReturned)
		
		self.out_queue.task_done()

		# print "finished"	

class MainWindow(object):
	def __init__(self,mwSession):
		self.mwSession			= mwSession
		self.root 				= None
		self.canvas 			= None
		self.prefroot 			= None
		self.helproot			= None
		self.aboutroot			= None
		self.input_queue		= Queue.Queue()
		self.output_queue		= Queue.Queue()
		self.prefChanged 		= 0
		self.newsArrived 		= 0
		self.allDisplayedNews 		= {}
		self.registeredCourses 		= {}
		self.initRegisteredCourses 	= {}
		self.allReadNews 			= {}
		self.allRunningThreads 		= {}

	def initMainWindow(self):
		self.loadInitRegisteredCourses()
		self.loadAllReadNews()

	def createMainWindow(self):
		self.root = Tk()
		self.root.title('Cow News Reader')
		self.root.protocol("WM_DELETE_WINDOW", self.closeMainWindow )

		w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

		self.canvas=Canvas(self.root,bg='#ABCDEF',width=w,height=h)

		hbar=Scrollbar(self.root,orient=HORIZONTAL)
		hbar.pack(side=BOTTOM,fill=X)
		hbar.config(command=self.canvas.xview)

		vbar=Scrollbar(self.root,orient=VERTICAL)
		vbar.pack(side=RIGHT,fill=Y)
		vbar.config(command=self.canvas.yview)

		self.canvas.config(scrollregion=(0,0,w,h))
		self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
		self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

		self.loadMenu()
		self.bindKeys()

		self.displayUnreadNews()

		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		self.root.mainloop()

	def loadMenu(self):
		menubar = Menu(self.root,background="#1B2D33")
		filemenu = Menu(menubar, tearoff=0)

		filemenu.add_command(label="Close", command=self.closeMainWindow)
		menubar.add_cascade(label="File", menu=filemenu, activebackground = "#D8E8ED")

		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label="Preferences", command=self.preferencesCommand)
		menubar.add_cascade(label="Edit", menu=editmenu, activebackground = "#D8E8ED")

		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="Help", command=self.helpCommand)
		helpmenu.add_command(label="About", command=self.aboutCommand)
		menubar.add_cascade(label="Help", menu=helpmenu, activebackground = "#D8E8ED")

		self.root.config(menu=menubar)

	def bindKeys(self):
		self.canvas.bind('<4>', lambda event : self.canvas.yview('scroll', -1, 'units'))
		self.canvas.bind('<5>', lambda event : self.canvas.yview('scroll', 1, 'units'))
		self.canvas.bind('<Up>', lambda event : self.canvas.yview('scroll', -1, 'units'))
		self.canvas.bind('<Down>', lambda event : self.canvas.yview('scroll', 1, 'units'))
		self.canvas.bind('<Left>', lambda event : self.canvas.xview('scroll', -1, 'units'))
		self.canvas.bind('<Right>', lambda event : self.canvas.xview('scroll', 1, 'units'))
		self.canvas.focus_set()

	def on_closing(self,windowToBeclosed):
		if windowToBeclosed == "prefroot":
			self.prefroot.destroy()
			self.prefroot = None
		elif windowToBeclosed == "helproot":
			self.helproot.destroy()
			self.helproot = None
		elif windowToBeclosed == "aboutroot":
			self.aboutroot.destroy()
			self.aboutroot = None

	def helpCommand(self):
		if self.helproot == None:
			self.helproot = Toplevel()
			self.helproot.title('Help')
			self.helproot.protocol("WM_DELETE_WINDOW", lambda: self.on_closing("helproot") )
			canvas = Canvas(self.helproot, width=300, height=300)
			canvas.pack()		

	def aboutCommand(self):
		if self.aboutroot == None:
			self.aboutroot = Toplevel()
			self.aboutroot.title('About')
			self.aboutroot.protocol("WM_DELETE_WINDOW", lambda: self.on_closing("aboutroot") )
			canvas = Canvas(self.aboutroot, width=300, height=300)
			canvas.pack()		

	def closeMainWindow(self):
		if self.prefroot != None:
			self.prefroot.destroy()
		if self.helproot != None:
			self.helproot.destroy()
		if self.aboutroot != None:
			self.aboutroot.destroy()

		self.saveAllReadNews()
		self.root.destroy()

	def preferencesCommand(self):
		if self.prefroot == None:
			self.prefroot = Toplevel()
			self.prefroot.title('Preferencess')
			self.prefroot.protocol("WM_DELETE_WINDOW", lambda: self.on_closing("prefroot") )
			self.prefroot.geometry('800x450')
			self.loadRegisteredCourses()
			self.createCheckButtons()
			Button(self.prefroot, text="SaveAndExit", command=self.registerCoursesAndExit).grid(row=20, column=20)

	def createCheckButtons(self):
		row     = 0
		col     = 0
		count   = 0
		global allCourses
		for course in allCourses:
		    if count%15 == 0:
		        row     = 5
		        col     += 5

		    Checkbutton(self.prefroot, text = course, variable = self.registeredCourses[course]).grid(row=row, column=col)
		    row     += 1
		    count   += 1

	def loadRegisteredCourses(self):

		global allCourses
		self.registeredCourses = { c:IntVar() for c in allCourses }
		f = open(os.path.expanduser('~') + "/.CowNewsReader/pref.txt", 'r')
		for line in f:
		    try:
		        v = IntVar()
		        v.set(1)   
		        self.registeredCourses[line.rstrip()] = v
		        
		    except KeyError, e:
		        raise e
		f.close()
     
	def loadInitRegisteredCourses(self):
		global allCourses
		self.initRegisteredCourses = { c:0 for c in allCourses }

		f = open(os.path.expanduser('~') + "/.CowNewsReader/pref.txt", 'r')
		for line in f:
		    try:
		        self.initRegisteredCourses[line.rstrip()] = 1
		        
		    except KeyError, e:
		        raise e
		f.close()

	def registerCoursesAndExit(self):
		f = open(os.path.expanduser('~') + "/.CowNewsReader/pref.txt", 'w')
		for key, value in self.registeredCourses.items():
		    val = value.get()
		    if val:
		        f.write(key+"\n")    	

		f.close()

		#Signal on pref change
		self.prefChanged = 1 

		self.prefroot.destroy()
		self.prefroot = None

	def loadAllReadNews(self):
		global allCourses
		for course in allCourses:
			self.allReadNews[course] = {}

		if os.stat(os.path.expanduser('~') + "/.CowNewsReader/read.txt").st_size != 0:
			try:
				with open(os.path.expanduser('~') + "/.CowNewsReader/read.txt", 'r') as infile:
				    self.allReadNews = dict(self.allReadNews.items() + json.load(infile).items())
			except ValueError, e:
				print e

	def saveAllReadNews(self):
		with open(os.path.expanduser('~') + "/.CowNewsReader/read.txt", 'w') as outfile:
			json.dump(self.allReadNews, outfile)

	def startMainWindow(self):
		#Check if new courses are added or removed. Reload course list
		if self.prefChanged:
			self.loadInitRegisteredCourses()
			self.prefChanged = 0

		#Work only with the registered courses
		for key, value in self.initRegisteredCourses.items():
		    val = value#.get()
		    if val:
				#Create object request
				req = Request(key, self.allReadNews[key], self.mwSession)

				#Initialize input_queue with the corresponding request
				self.input_queue.put(req)
				
		#Create threads for each selected course
		for key, value in self.initRegisteredCourses.items():
			val = value#.get()
			if val:
				if not key in self.allRunningThreads:	#if thread does not exist, create
					self.allRunningThreads[key] = 1
				elif self.allRunningThreads[key]:		#if thread is still running, continue
					continue	

				myThread = CheckNews(self.input_queue, self.output_queue)
				myThread.setDaemon(True)
				myThread.start()

	def processResult(self):
		# print "coming to process"
		try:

			while self.output_queue.qsize():
				_req = self.output_queue.get(0)

				if not isinstance(_req, list):
					self.allRunningThreads[_req] = 0

				else:
					for req in _req:
						self.allReadNews[req.courseName][req.newsId] 	= 0
						self.allRunningThreads[req.courseName]			= 0

						newsToBeDisplayed = NewsReader(req.courseName, req.responseImg, req.responseSubjectMessage, req.responseFromMessage, req.responseDateMessage, req.responseMessageBody)
						self.allDisplayedNews[newsToBeDisplayed] = 0

						# Create desktop notification
						os.system("notify-send -i " + req.responseImg.replace('&', '\&') + " \""  
							+ req.responseFromName.encode("UTF-8") + ": " 
							+ req.responseSubjectMessage.encode("UTF-8") + "\" \""  
							+ req.responseMessageBody.encode("UTF-8").strip() + "\"")

						# Signal new news has arrived
						self.newsArrived = 1

		except Queue.Empty:
			print "Error: Queue Empty"			

	def displayUnreadNews(self):
		global lastNewsPosition
		lastNewsPosition = 0

		for key, value in self.allDisplayedNews.items():
			if not value:
				key.setCanvas(self.canvas)
				key.createNews()
				self.allDisplayedNews[key] = 1

		#Restore back newsArrived
		self.newsArrived = 0
