import objc, re, os

import Listener
#import Interact
import Calibration
import platform
import SimpleDialog
import Foundation, objc
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper

#CONST
Z_LIMIT_CUT = 0
OS_NAME_OSX = 'darwin'
OS_NAME_WIN = 'windows'

# Icon
MENU_ICON = 'resources/iconleaptouch.png'

STATE_CALIB_TL = 0
STATE_CALIB_TR = 1
STATE_CALIB_BR = 2
STATE_CALIB_BL = 3
STATE_INI = 4
STATE_USING = 5

class Main(NSObject):

  def applicationDidFinishLaunching_(self, notification):
    # Set up status bar item
    self.statusbar = NSStatusBar.systemStatusBar()
    self.statusitem = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    self.statusitem.setImage_(NSImage.alloc().initByReferencingFile_(MENU_ICON))
    self.statusitem.setHighlightMode_(1)
    self.statusitem.setToolTip_('Leaptouch')

    # Build a very simple menu
    self.menu = NSMenu.alloc().init()
    # Sync event is bound to sync_ method
    self.calibrate_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Recalibrate', 'calibrate:', '')
    self.menu.addItem_(self.calibrate_menu_item)
    # Default event
    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
    self.menu.addItem_(menuitem)
    # Bind it to the status item
    self.statusitem.setMenu_(self.menu)

    self.state = STATE_INI
    self.listener = Listener.Listener(self.on_frame)
    self.calibration_points = []
    self.translator = Calibration.Translator()

    os_name = platform.system().lower()
    if os_name == OS_NAME_OSX:
      from lib.OSX import Interact
      self.interact = Interact.Interact()
    elif os_name == OS_NAME_WIN:
      from lib.WIN import interact
      self.interact = Interact.Interact()

    self.calibrate()


  def on_frame(self, point_tuple):
    if not point_tuple:
      return

    point, fingers = point_tuple

    if self.state == STATE_INI:
      self.state = STATE_CALIB_TL
      self.calibration_points = []
      self.notify('LeapTouch', 'Calibrating your screen!', 'Put a finger on the top left of your monitor')
    elif self.state == STATE_CALIB_TL:
      self.calibration_points.append(point)
      self.calibration_points = self.calibration_points[-100:]
      if self.translator.attempt_calibration(self.calibration_points, 0):
        self.notify('LeapTouch', 'Calibrating your screen!', 'Now on the top right of your monitor')
        self.calibration_points = []
        self.state = STATE_CALIB_TR
    elif self.state == STATE_CALIB_TR:
      self.calibration_points.append(point)
      self.calibration_points = self.calibration_points[-100:]
      if self.translator.attempt_calibration(self.calibration_points, 1):
        self.notify('LeapTouch', 'Calibrating your screen!', 'Now on the bottom right of your monitor')
        self.calibration_points = []
        self.state = STATE_CALIB_BR
    elif self.state == STATE_CALIB_BR:
      self.calibration_points.append(point)
      self.calibration_points = self.calibration_points[-100:]
      if self.translator.attempt_calibration(self.calibration_points, 2):
        self.notify('LeapTouch', 'Calibrating your screen!', 'And finally, bottom left!')
        self.calibration_points = []
        self.state = STATE_CALIB_BL
    elif self.state == STATE_CALIB_BL:
      self.calibration_points.append(point)
      self.calibration_points = self.calibration_points[-100:]
      if self.translator.attempt_calibration(self.calibration_points, 3):
        self.notify('LeapTouch', 'Screen calibrated!', 'Ready to go, touch the screen!')
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

  def notify(self, title, subtitle, info_text, delay=0, sound=False, userInfo={}):
    print title, subtitle, info_text
    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    notification.setUserInfo_(userInfo)

    if sound:
      notification.setSoundName_("NSUserNotificationDefaultSoundName")

    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

if __name__ == "__main__":
  app = NSApplication.sharedApplication()
  delegate = Main.alloc().init()
  app.setDelegate_(delegate)
  AppHelper.runEventLoop()
