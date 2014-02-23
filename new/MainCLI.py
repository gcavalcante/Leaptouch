import platform

import Listener
import Calibration
import SimpleDialog

#CONST
Z_LIMIT_CUT = 0
OS_NAME_OSX = 'darwin'
OS_NAME_WIN = 'windows'

STATE_CALIB_TL = 0
STATE_CALIB_TR = 1
STATE_CALIB_BR = 2
STATE_CALIB_BL = 3
STATE_INI = 4
STATE_USING = 5

class Main():

  def __init__(self):
    self.state = STATE_INI
    self.listener = Listener.Listener(self.on_frame)
    self.calibration_points = []
    self.translator = Calibration.Translator()

    os_name = platform.system().lower()
    if os_name == OS_NAME_OSX:
      from lib.OSX import Interact
      self.interact = Interact.Interact()
    elif os_name == OS_NAME_WIN:
      from lib.WIN import Interact
      self.interact = Interact.Interact()

    self.calibrate()


  def on_frame(self, point_tuple):
    if not point_tuple:
      return

    point, fingers = point_tuple

    if self.state == STATE_INI:
      self.state = STATE_CALIB_TL
      self.calibration_points = []
      print 'Put a finger on the top left of your monitor'
    elif self.state == STATE_CALIB_TL:
      self.calibration_points.append(point)
      self.calibration_points = self.calibration_points[-100:]
      if self.translator.attempt_calibration(self.calibration_points, 0):
        print 'Now on the top right of your monitor'
        self.calibration_points = []
        self.state = STATE_CALIB_TR
    elif self.state == STATE_CALIB_TR:
      self.calibration_points.append(point)
      self.calibration_points = self.calibration_points[-100:]
      if self.translator.attempt_calibration(self.calibration_points, 1):
        print 'Now on the bottom right of your monitor'
        self.calibration_points = []
        self.state = STATE_CALIB_BR
    elif self.state == STATE_CALIB_BR:
      self.calibration_points.append(point)
      self.calibration_points = self.calibration_points[-100:]
      if self.translator.attempt_calibration(self.calibration_points, 2):
        print 'And finally, bottom left!'
        self.calibration_points = []
        self.state = STATE_CALIB_BL
    elif self.state == STATE_CALIB_BL:
      self.calibration_points.append(point)
      self.calibration_points = self.calibration_points[-100:]
      if self.translator.attempt_calibration(self.calibration_points, 3):
        print 'Ready to go, touch the screen!'
        self.translator.finalizecalibration()
        self.state = STATE_USING
    elif self.state == STATE_USING:
      x, y, z = self.translator.leaptransform(point)
      print x, y, z
      down = False
      if z < Z_LIMIT_CUT:
        down = True

      self.interact.update(x, y, down, fingers)

  def calibrate(self):
    self.state = STATE_INI

if __name__ == "__main__":
  main = Main()
  foo = raw_input()
  main.end_calibration()
  foo = raw_input()
