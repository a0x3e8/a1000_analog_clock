#!/usr/bin/python

import time
import math
import gtk
import cairo
import gobject
import sys, getopt
class AnaClock(object):
	mode=0  #default is gtk interface mode. 1 will be imagemode.
	show_sec=False
	GWIDTH= 100
	GHEIGHT= 100
	'''this is the analog clock main class.
	this clock will be resizable and will have costumizable themes.
	'''
#variables:
#self._center=a tuple like this:(center x,center y)
#self.clockFaceRad=radius of the clock face.
	def __init__(self,argv):
		self.cli_parser(argv)
		print self.mode
		if self.mode==0:
			self.gtk_ui_init()
		else:
			self.image_init()
	def cli_parser(self,argv):
		'''this function will set attributes using command line arguments.
I will use 6 arguments:
-h or --help for showing help and usage.
-i or --imagemode for image creation mode.
-c or --colors for setting the colors.
-s or --show_secound for showing second hand.
-w or --width for set width.
-H or --height for setting height.'''
		try:
			opts,args=getopt.getopt(argv,'hic:sw:H:',['help','imagemode','colors=','show_second','width=','height='])
		except getopt.GetoptError:
			self.usage()
			sys.exit(2)
		for opt,arg in opts:
			if opt in('-h','--help'):
				self.usage()
				sys.exit(0)
			elif opt in ('-i','--imagemode'):
				self.mode=1 #setting mode to image mode
			elif opt in ('-c','--colors'):
				print 'color is a TODO!'
			elif opt in ('-s','--show_second'):
				self.show_sec=True
			elif opt in ('-w','--width'):
				if int(arg)<800 and int(arg)>50:
					self.GWIDTH=int(arg)
					print 'GWIDTH sat to ',arg
			elif opt in ('-H','--height'):
				if int(arg)<800 and int(arg)>50:
					self.GHEIGHT=int(arg)

	def usage(self):
		print '''a1000 anaClock application is a simple analog clock creator for using as a widget or
image clock generator for conky.
this software is a free software under GNU GPL version 3 license and any compatible license. after that'''
	def gtk_ui_init(self):
		self.root=gtk.Window()	
		self.root.set_size_request(self.GWIDTH,self.GHEIGHT)
		self.root.set_title("AnaClock")
		bgcolor=gtk.gdk.color_parse("#393939")
		self.root.modify_bg(gtk.STATE_NORMAL,bgcolor)
		self.root.connect('destroy',gtk.main_quit)
		self.dArea=gtk.DrawingArea()
		self.dArea.connect('expose-event',self.expose)
		self.root.connect('check-resize',self.resize)
		self.timer=gobject.timeout_add(1000,self.expose,self.dArea,None)

		#now default clock center and size. if resized, resize function will change this.
		self._center=self.root.get_size_request()
		self.clockFaceRad=self._center[0]-self._center[0]/50
#variables to config:
		self.smallHandR=self.clockFaceRad*3/5
		self.bigHandRad=self.clockFaceRad*3/4
		self.secHandRad=self.clockFaceRad*6/8
#colors to set:
		smallHandColor='some color'
		bigHandColor='some color'
		secHandColor='some color'

#################################################


		self.root.add(self.dArea)
		self.root.show_all()
		gtk.main()
#end of init function.###################################

#expose event will draw clock nice and easy...
	def image_init(self):
		self.root=cairo.ImageSurface(cairo.FORMAT_ARGB32,self.GWIDTH,self.GHEIGHT)
#now default clock center and size. if resized, resize function will change this.
		self._center=(self.GWIDTH/2,self.GHEIGHT/2)
		self.clockFaceRad=self._center[0]-self._center[0]/50
#variables to config:
		self.smallHandR=self.clockFaceRad*3/5
		self.bigHandRad=self.clockFaceRad*3/4
		self.secHandRad=self.clockFaceRad*6/8
#colors to set:
		smallHandColor='some color'
		bigHandColor='some color'
		secHandColor='some color'

		self.expose(self.root)

		try:
			self.root.write_to_png('clock_face.png')
		except:
			print 'error writing to file.'
			exit(2)

	def expose(self,widget,data=None):
		if self.mode==0:
			self.surface=widget.window.cairo_create()
		else:
			self.surface=cairo.Context(widget)
		self.surface.set_source_rgb(1,1,1)
		self.surface.arc(self._center[0],self._center[1],self.clockFaceRad,0,2*math.pi)
		self.surface.fill()
		self.surface.stroke()
#drawing numbers:
		self.surface.set_source_rgb(0.2,0.2,0.2)
		self.surface.set_line_width(self.clockFaceRad/15)
		for a in range(0,12):
			self.surface.arc(self._center[0],self._center[1],self.clockFaceRad-self.clockFaceRad/10,a*math.pi/6-0.01*math.pi,a*math.pi/6+0.01*math.pi)
			self.surface.stroke()
#drawing the border:
		self.surface.set_source_rgb(0.6, 0.6, 0.6)
		borderMinus=self.clockFaceRad/10
		self.surface.set_line_width(borderMinus)
		self.surface.arc(self._center[0],self._center[1],self.clockFaceRad-borderMinus/2,0,2*math.pi)
		self.surface.stroke()
		
		self.surface.set_line_width(borderMinus/2)
		self.surface.set_source_rgb(0.3, 0.3, 0.3)
		self.surface.arc(self._center[0],self._center[1],self.clockFaceRad-borderMinus/2,0,2*math.pi)
		self.surface.stroke()
#calling hand drawer:
		self.hand_drawer()
		self.surface.move_to(self._center[0],self._center[1])
		centerCircleR=self.clockFaceRad*5/100
		self.surface.arc(self._center[0],self._center[1],centerCircleR,0,2*math.pi)
		self.surface.fill()
		self.surface.stroke()
		return True
	def hand_drawer(self):
		'''this function will draw the clock hands from the time given by the 
get_time function.'''

		#variables:
		time_tuple=self.get_time()
		hour=time_tuple[0]
		if hour>12:hour-=12
		minutes=time_tuple[1]
		sec=time_tuple[2]
		self.surface.move_to(self._center[0],self._center[1])
		#draw clock hands:
#hour hand:
		self.surface.set_source_rgb(0,0,0)
		self.surface.set_line_width(self.clockFaceRad/15)
		handEndx=self._center[0]+self.smallHandR*math.cos(((hour-3)*math.pi)/6+(minutes*math.pi)/360)
		handEndy=self._center[1]+self.smallHandR*math.sin(((hour-3)*math.pi)/6+(minutes*math.pi)/360)
		self.surface.line_to(handEndx,handEndy)
		self.surface.stroke()

#minute hand:
		handEndx=self._center[0]+self.bigHandRad*math.cos(((minutes-15)*math.pi)/30)
		handEndy=self._center[1]+self.bigHandRad*math.sin(((minutes-15)*math.pi)/30)
		self.surface.move_to(self._center[0],self._center[1])
		self.surface.set_source_rgb(0,0,0)
		self.surface.set_line_width(self.clockFaceRad/18)
		self.surface.line_to(handEndx,handEndy)
		self.surface.stroke()
#sec hand:
		if self.show_sec:
			handEndx=self._center[0]+self.secHandRad*math.cos(((sec-15)*math.pi)/30)
			handEndy=self._center[1]+self.secHandRad*math.sin(((sec-15)*math.pi)/30)
			self.surface.move_to(self._center[0],self._center[1])
			self.surface.set_source_rgb(0.8,0.2,0.2)
			self.surface.set_line_width(self.clockFaceRad/25)
			self.surface.line_to(handEndx,handEndy)
			self.surface.stroke()




	def get_time(self):
		'''gets current time and stores it in a tuple'''
		currentTime=time.localtime()
		return (currentTime.tm_hour,currentTime.tm_min,currentTime.tm_sec)

	def resize(self,widget,data=None):
		'''this function will resize the clock
		according to window size.
		and makes sure clock is always visible by
		setting radious to smaller one from width
		and height of the window.'''
		self._center=self.root.get_size()
		self._center=(self._center[0]/2,self._center[1]/2)

		if self._center[0]<self._center[1]:
			self.clockFaceRad=self._center[0]-self._center[0]/50	
		else:
			self.clockFaceRad=self._center[1]-self._center[1]/50
#setting variables if window got resized:
		self.smallHandR=self.clockFaceRad*3/5
		self.bigHandRad=self.clockFaceRad*3/4
		self.secHandRad=self.clockFaceRad*6/8

		self.expose(self.root)
####################################################
class image_clock(AnaClock):
	def __init__(self):
		self.surface=cairo.Image_surface()
		self.surface.set_size_request(GWIDTH,GHEIGHT)

if __name__=='__main__':
	ac=AnaClock(sys.argv[1:])
