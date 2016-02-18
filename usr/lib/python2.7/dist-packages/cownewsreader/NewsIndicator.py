from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
import threading
import os,sys

class NewsIndicator(object):
	def __init__(self, mw):
		self.mw 		= mw
		self.indNews 	= 0
		self.indicator 	= appindicator.Indicator.new('News Indicator', os.path.abspath('/usr/share/cownewsreader/media/mail2.png'), appindicator.IndicatorCategory.APPLICATION_STATUS)
		self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
		self.indicator.set_attention_icon(os.path.abspath('/usr/share/cownewsreader/media/mail1.png'))
		self.build_menu()
		self.indicator.set_menu(self.menu)

	def build_menu(self):
	    self.menu = gtk.Menu()
	    self.item_main_window = gtk.MenuItem('Open Main Window')
	    self.item_main_window.connect('activate', self.main_window)
	    self.menu.append(self.item_main_window)
	    self.menu.append(gtk.SeparatorMenuItem().new())
	    self.item_quit = gtk.MenuItem('Quit')
	    self.item_quit.connect('activate', self.quit)
	    self.menu.append(self.item_quit)
	    self.menu.show_all()
	    
	def main_window(self,widget):
		self.mw.createMainWindow()

	def quit(self,widget):
		gtk.main_quit()
		sys.exit(0)

	def initPeriodicCheck(self):
		t = threading.Timer(60, self.periodicCheck)
		t.setDaemon(True)
		t.start()
		self.mw.startMainWindow()

	def periodicCheck(self):
		t = threading.Timer(60, self.periodicCheck)
		t.setDaemon(True)
		t.start()
		self.mw.processResult()

		#Check if new news was notified
		if self.mw.newsArrived and not self.indNews:
			self.indNews = 1
			self.indicator.set_status(appindicator.IndicatorStatus.ATTENTION)
		elif not self.mw.newsArrived and self.indNews:
			self.indNews = 0
			self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

		self.mw.startMainWindow()
	
	def main(self):
		#Set up periodic check
		self.initPeriodicCheck()
	 	gtk.main()
