import Listener
#import Interact
import Calibration
import platform
import SimpleDialog

#CONST
Z_LIMIT_CUT = 20
OS_NAME_OSX = 'darwin'
OS_NAME_WIN = 'fuck'

import objc, re, os
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper

# Icon
MENU_ICON = 'resources/iconleaptouch.png'

STATE_INI = 4
STATE_CALIB_TL = 0
STATE_CALIB_TR = 1
STATE_CALIB_BR = 2
STATE_CALIB_BL = 3
STATE_USING = 5

CALIB_TIMEOUT = 300

#start_time = NSDate.date()

class Main(NSObject):
  statusbar = None

  def applicationDidFinishLaunching_(self, notification):
    statusbar = NSStatusBar.systemStatusBar()
    # Create the statusbar item
    self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    # Set initial image
    self.statusitem.setImage_(NSImage.alloc().initByReferencingFile_(MENU_ICON))
    # Let it highlight upon clicking
    self.statusitem.setHighlightMode_(1)
    # Set a tooltip
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
    #self.calibrator = Calibration.Calibration()
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

    self.calibrate_('')

    # Get the timer going
    #self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 5.0, self, 'tick:', None, True)
    #NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    #self.timer.fire()

  def on_frame(self,point_tuple):
    if self.state != STATE_INI and self.state != STATE_USING and point_tuple:
      point,fingers = point_tuple
      print point_tuple
      if self.calib_timer > 0:
        self.calib_timer -= 1
      else:
        self.translator.calibratepoints(point, self.state)
        if self.state == STATE_CALIB_TL:
          self.state = STATE_CALIB_TR
          notify('LeapTouch', 'Calibrating your screen!', 'Now on the top right of your monitor')
        elif self.state == STATE_CALIB_TR:
          self.state = STATE_CALIB_BR
          notify('LeapTouch', 'Calibrating your screen!', 'Ok, bottom right now...')
        elif self.state == STATE_CALIB_BR:
          self.state = STATE_CALIB_BL
          notify('LeapTouch', 'Calibrating your screen!', 'And finally, bottom left!')
        elif self.state == STATE_CALIB_BL:
          self.state = STATE_USING
          notify('LeapTouch', 'Screen calibrated!', 'Ready to go, touch the screen!')
        self.calib_timer = CALIB_TIMEOUT
      # TCHA
      #self.calibrator.calibratepoints(self, point, self.state)
      #self.calibration_points.append(point)
    elif self.state == STATE_USING and point_tuple:
      point,fingers = point_tuple
      print point
      #x,y,z_transform = self.translator.leaptransform(point)
      #z = point[2] - z_transform
      #print z_transform
      x, y, z = self.translator.leaptransform(point) #self.calibrator.leaptoscreen(point[0],point[1])
      if z < Z_LIMIT_CUT:
        self.down = True
      elif z > Z_LIMIT_CUT:
        self.down = False
      print 'DOWN = ', self.down
      self.interact.update(x,y,self.down,fingers)

  def calibrate_(self, notification):
    if self.state == STATE_INI or self.state == STATE_USING:
      self.state = STATE_CALIB_TL
      self.calib_timer = CALIB_TIMEOUT
      notify('LeapTouch', 'Calibrating your screen!', 'Put a finger on the top left of your monitor')
    else:
      self.state = STATE_USING
      self.calibrate_menu_item.setTitle_('Recalibrate')
      self.end_calibration()

  def __del__(self):
    del self.listener

  def end_calibration(self):
    self.state = STATE_USING
    self.translator.calibratepoints(self.calibration_points)
    #self.calibrator.set_calibration(self.calibration_points)
    #self.z_limit = self.get_extreme_z(self.calibration_points)
    #Call the Calibrate funtion in Translation Module (self.calibration_points)

  #def get_extreme_z(self,points):
  #  biggers = [-9999,-9999,-9999]
  #  smallers = [9999,9999,9999]
  #  zs = [z[2] for z in points]
  #  points.sort()
    # min_z = 0
    # #z[0] + 20
    # for x,y,z in points:
    #   if z < min_z:#Consider Only points near screen
    #     biggers[0] = x if x > biggers[0] else biggers[0]
    #     biggers[1] = y if y > biggers[1] else biggers[1]
    #     biggers[2] = z if z > biggers[2] else biggers[2]
    #     smallers[0] = x if x < smallers[0] else smallers[0]
    #     smallers[1] = y if y < smallers[1] else smallers[1]
    #     smallers[2] = z if z < smallers[2] else smallers[2]
    # return smallers[2]

# Python integration with Mountain Lion's notification center

import Foundation, objc

NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={}):
  """ Python method to show a desktop notification on Mountain Lion. Where:
        title: Title of notification
        subtitle: Subtitle of notification
        info_text: Informative text of notification
        delay: Delay (in seconds) before showing the notification
        sound: Play the default notification sound
        userInfo: a dictionary that can be used to handle clicks in your
                  app's applicationDidFinishLaunching:aNotification method
  """
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
