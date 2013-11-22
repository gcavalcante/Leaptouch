import Listener
#import Interact
import Calibration
import platform

#CONST
Z_LIMIT_CUT = 20
OS_NAME_OSX = 'darwin'
OS_NAME_WIN = 'fuck'

class Main():
  def on_frame(self,point_tuple):
    if self.in_calibration and point_tuple:
      point,fingers = point_tuple
      print point_tuple
      self.calibration_points.append(point)
    elif not self.in_calibration and point_tuple:
      point,fingers = point_tuple
      x,y = self.calibrator.leaptoscreen(point[0],point[1])
      z = point[2]
      
      Z_LIMIT_CUT = -1.0*z*60/249+20
      print Z_LIMIT_CUT, self.z_limit
      if z < -240:
        self.down = True
      elif z > -240:
        self.down = False

      print 'DOWN = ', self.down
      self.interact.update(x,y,self.down,fingers)


      #Call the translator and interact

#      if z < self.z_limit + Z_LIMIT_CUT : 
#        self.interact.mousemove(x,y)
#      if z < self.z_limit + Z_LIMIT_CUT and not self.down:
#        self.interact.mousedown(x,y)
#        self.down = True
#      if z < self.z_limit + Z_LIMIT_CUT and self.down:
#        self.interact.mousedragEvent(x,y)
#      if z < self.z_limit + Z_LIMIT_CUT and self.down:
#        self.interact.mouseup(x,y)
#        self.down = False

        
        

  def __init__(self):
    self.in_calibration = True
    self.listener = Listener.Listener(self.on_frame)
    self.calibration_points = []
    self.calibrator = Calibration.Calibration()
    #Decide what Interact to Call
    os_name = platform.system().lower()
    if os_name == OS_NAME_OSX:
      from lib.OSX import Interact
      self.interact = Interact.Interact()
    elif os_name == OS_NAME_WIN:
      pass
      from lib.WIN import interact
      self.interact = Interact.Interact()
    #Mouse Init
    self.down = False
  def __del__(self):
    del self.listener

  def end_calibration(self):
    self.in_calibration = False
    self.z_limit = self.calibrator.set_calibration(self.calibration_points)
    #Call the Calibrate funtion in Translation Module (self.calibration_points)

if __name__ == "__main__":
  main = Main()
  foo = raw_input()
  main.end_calibration()
  foo = raw_input()
