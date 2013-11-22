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
      x,y,z_transform = self.translator.leaptransform(point)
      z = point[2] - z_transform
      print z_transform
      x,y = self.calibrator.leaptoscreen(point[0],point[1])
      if z < self.z_limit :
        self.down = True
      elif z >  self.z_limit:
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
    self.translator = Calibration.Translator()
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
    self.translator.calibratepoints(self.calibration_points)
    self.calibrator.set_calibration(self.calibration_points)
    self.z_limit = self.get_extreme_z(self.calibration_points)
    #Call the Calibrate funtion in Translation Module (self.calibration_points)

  def get_extreme_z(self,points):
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
    return smallers[2]



if __name__ == "__main__":
  main = Main()
  foo = raw_input()
  main.end_calibration()
  foo = raw_input()
