
import platform

import numpy
from numpy import linalg

os = 'MAC'





class Translator:

	def __init__(self):
		self.display = []
		self.leap = []

	def add_point(self, display, leap):
		self.display.append(display)
		self.leap.append(leap)

	def calculate(self):
		A = numpy.zeros((3,3))
		A[0] = self.BR - self.BL
		A[1] = self.TL - self.BL
		A[2] = numpy.cross(A[0], A[1])
		A[2] /= numpy.linalg.norm(A[2])

		self.A = A

	def project(self, p):
		q = p
		p = self.BL
		n = self.A[2]

		q_proj = q - numpy.dot(q - p, n) * n
		return q_proj

	def get_x(self, p):
		p = numpy.array(p) 

		proj = self.project(p) - self.BL
		#print p, proj

		return numpy.dot(proj, self.A[0]/numpy.linalg.norm(self.A[0])) / numpy.linalg.norm(self.A[0])


	def get_y(self, p):
		p = numpy.array(p) 

		proj = self.project(p) - self.BL
		#print p, proj

		return numpy.dot(proj, self.A[1]/numpy.linalg.norm(self.A[1])) / numpy.linalg.norm(self.A[1])

	def get_z(self, p):
		p = numpy.array(p)
		proj = self.project(p)
		d = proj - p
		return numpy.linalg.norm(d)

	# Calculate borders from points
	def calibratepoints(self, npoints):
		UL = [0.0,0.0,0.0]
		UR = [0.0,0.0,0.0]
		BL = [0.0,800000.0,0.0]
		BR = [0.0,800000.0,0.0]
		for p in npoints :
			if p[0] < 0 and p[1] > UL[1]:
				UL = p
			if p[0]	> 0 and p[1] > UR[1]:
				UR = p
			if p[0] < 0 and p[1] < BL[1]:
				BL = p
			if p[0]	> 0 and p[1] < BR[1]:
				BR = p
		self.TL = numpy.array(UL)
		self.TR = numpy.array(UR)
		self.BL = numpy.array(BL)
		self.BR = numpy.array(BR)
		self.calculate()

	def leaptransform(self, p):
		return [self.get_x(p), self.get_y(p), self.get_z(p)]


















class Calibration():
  def __init__(self):
    #Get screen reso
    if os == 'MAC':
      self.resolution = Displays.resolutions()[-1]
    elif os == 'WIN':
      pass
  def get_extremes(self,points):
    biggers = [-9999,-9999,-9999]
    smallers = [9999,9999,9999]
    zs = [z[2] for z in points]
    points.sort()
    min_z = 0
    #z[0] + 20
    for x,y,z in points:
      if z < min_z:#Consider Only points near screen
        biggers[0] = x if x > biggers[0] else biggers[0]
        biggers[1] = y if y > biggers[1] else biggers[1]
        biggers[2] = z if z > biggers[2] else biggers[2]
        smallers[0] = x if x < smallers[0] else smallers[0]
        smallers[1] = y if y < smallers[1] else smallers[1]
        smallers[2] = z if z < smallers[2] else smallers[2]
    return biggers,smallers

  def set_calibration(self,points):
    biggers,smallers = self.get_extremes(points)
    #print biggers,smallers
    self.leaplm = smallers[0]
    self.leaprm = biggers[0]
    self.leapum = biggers[1] 
    self.leapdm = smallers[1]
    self.monlm = 0
    self.monrm,self.mondm = self.resolution
    self.monum = 0
    self.leapw = ((self.leaprm - self.leaplm) / 2)
    self.leaph = ((self.leapum - self.leapdm) / 2)
    self.monw = ((self.monrm - self.monlm) / 2)
    self.monh = ((self.mondm - self.monum) / 2)
    return smallers[2]
  def leaptoscreen(self,posx,posy):
  	if posx >= self.leaplm and posx <= self.leaprm :
  		monx = (posx - self.leaplm) * self.monw / self.leapw
  	else :
  		monx = -1
  	if posy >= self.leapdm and posy <= self.leapum :
  		mony = abs(posy - self.leapum) * self.monh / self.leaph
  	else :
  		mony = -1
  	return [monx, mony]




# Usage: Displays.resolutions() -> [(x1, y1), (x2, y2)]
class Displays(object):

  # OS Names
  OS_NAME_OSX = 'darwin'
  OS_NAME_WIN = '??'

  @staticmethod
  def resolutions():
    os_name = platform.system().lower()
    # OSX
    if os_name == Displays.OS_NAME_OSX:
      import AppKit
      return [(screen.frame().size.width, screen.frame().size.height) for screen in AppKit.NSScreen.screens()]
    # WIN
    elif os_name == Displays.OS_NAME_WIN:
      # TODO TEST THIS ON WINDOWS!
      import ctypes
      user32 = ctypes.windll.user32
      return (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

