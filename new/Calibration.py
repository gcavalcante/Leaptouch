
import platform


os = 'MAC'



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

