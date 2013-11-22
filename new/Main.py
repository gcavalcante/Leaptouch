import Listener
import Interact
import Calibration


Z_LIMIT_CUT = 20

class Main():
  def on_frame(self,point):
    if self.in_calibration and point:
      self.calibration_points.append(point)
    elif not self.in_calibration and point:
      print point
      x,y = self.calibrator.leaptoscreen(point[0],point[1])
      z = point[2]
      
      Z_LIMIT_CUT = -1.0*z*60/249+20
      print Z_LIMIT_CUT, self.z_limit
      #Call the translator and interact

      if z < self.z_limit + Z_LIMIT_CUT : 
        self.interact.mousemove(x,y)
      if z < self.z_limit + Z_LIMIT_CUT and not self.down:
        self.interact.mousedown(x,y)
        self.down = True
      if z < self.z_limit + Z_LIMIT_CUT and self.down:
        self.interact.mousedragEvent(x,y)
      if z < self.z_limit + Z_LIMIT_CUT and self.down:
        self.interact.mouseup(x,y)
        self.down = False

        
        

  def __init__(self):
    self.in_calibration = True
    self.listener = Listener.Listener(self.on_frame)
    self.calibration_points = []
    self.calibrator = Calibration.Calibration()
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
