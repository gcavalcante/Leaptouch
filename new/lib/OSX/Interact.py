import AppKit, subprocess, os
from Quartz.CoreGraphics import (CGEventCreateMouseEvent,CGEventPost,CGDisplayBounds,
    CGEventCreateScrollWheelEvent,CGEventSourceCreate,kCGScrollEventUnitPixel,
    kCGScrollEventUnitLine,kCGEventMouseMoved,kCGEventLeftMouseDragged,
    kCGEventLeftMouseDown,kCGEventLeftMouseUp,kCGMouseButtonLeft,kCGEventRightMouseDown,
    kCGEventRightMouseDown,kCGEventRightMouseUp,kCGMouseButtonRight,kCGHIDEventTap)

# OSX interaction class
class Interact():

  GEST_MISSION_CONTROL = 'MCGest'
  GEST_SWIPE_LEFT = 'SLGest'
  GEST_SWIPE_RIGHT = 'SRGest'
  GEST_APP_VIEW = 'AVGest'
  GEST_TIMEOUT = 30
  GEST_SPEED_TRHS = 30

  def __init__(self):
    self.screen_width, self.screen_height = [(screen.frame().size.width, screen.frame().size.height) for screen in AppKit.NSScreen.screens()][-1]
    self.left_button_pressed = False
    self.mouse_x = 0
    self.mouse_y = 0
    self.last_mouse_state = False
    self.buffer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.gesture_timeout = 0
    for i in range(10):
      self.buffer[i] = [0,0,0,0]

  def addtobuffer(self, finger_x, finger_y, pressed, fingers):
    if not hasattr(self, 'buffer'):
      for i in range(10):
        self.buffer[i] = [0,0,0,0]
    for i in range(9):
      self.buffer[i] = self.buffer[i+1]
    self.buffer[9] = [finger_x, finger_y, pressed, fingers]

  def getxvel(self):
    v = 0.0
    for i in range(9):
      v += self.buffer[i + 1][0] - self.buffer[i][0]
    return v / 9.0; 

  def getyvel(self):
    v = 0.0
    for i in range(9):
      v += self.buffer[i + 1][1] - self.buffer[i][1]
    return v / 9.0; 
	
  def update(self, finger_x, finger_y, pressed, fingers):
    finger_x *= self.screen_width
    finger_y = self.screen_height - (finger_y * self.screen_height)
    if not hasattr(self, 'last'):
      self.last = (finger_x,finger_y,pressed,fingers)
    if fingers == 1:
      self.set_left_button_pressed(pressed)
    elif fingers == 2 and self.last[3] == 2:
      Interact.execute_event(CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitPixel, 2, self.last[1]-finger_y, self.last[0]-finger_x))
    elif fingers >= 3 and self.last[3] >= 3 and self.gesture_timeout <= 0:
      if self.getxvel() > Interact.GEST_SPEED_TRHS:
        self.gestures(Interact.GEST_SWIPE_LEFT)
      elif self.getxvel() < - Interact.GEST_SPEED_TRHS:
        self.gestures(Interact.GEST_SWIPE_RIGHT)
      elif self.getyvel() > Interact.GEST_SPEED_TRHS:
        self.gestures(Interact.GEST_APP_VIEW)
      elif self.getyvel() < - Interact.GEST_SPEED_TRHS:
        self.gestures(Interact.GEST_MISSION_CONTROL)

    if self.gesture_timeout > 0:
      self.gesture_timeout -= 1

    print self.gesture_timeout

    self.move_mouse(finger_x, finger_y)
    self.last = (finger_x,finger_y,pressed,fingers)
    self.addtobuffer(finger_x,finger_y,pressed,fingers)


  def move_mouse(self, x, y):
    self.mouse_x = x
    self.mouse_y = y
    self.check_and_correct_borders();
    if self.left_button_pressed: # Drag!
      Interact.execute_event(CGEventCreateMouseEvent(None, kCGEventLeftMouseDragged, (self.mouse_x, self.mouse_y), 0))
    else: # Just move
      Interact.execute_event(CGEventCreateMouseEvent(None, kCGEventMouseMoved, (self.mouse_x, self.mouse_y), 0))

  def set_left_button_pressed(self, boolean_button): 
    if boolean_button == True and not self.last_mouse_state:
      self.click_down()
    elif not boolean_button and self.last_mouse_state: 
      self.click_up()
    self.last_mouse_state = boolean_button
        
  def click_down(self):
    Interact.execute_event(CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (self.mouse_x, self.mouse_y), 0))
    self.left_button_pressed = True

  def click_up(self):
    Interact.execute_event(CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (self.mouse_x, self.mouse_y), 0))
    self.left_button_pressed = False
  
  def check_and_correct_borders(self):
    if self.mouse_x > self.screen_width: 
      self.mouse_x = self.screen_width - 1
    if self.mouse_x < 0.0: 
      self.mouse_x = 0.0
    if self.mouse_y > self.screen_height: 
      self.mouse_y = self.screen_height - 1
    if self.mouse_y < 0.0: 
      self.mouse_y = 0.0

  @staticmethod
  def execute_event(event):
    CGEventPost(kCGHIDEventTap, event)

  # OSX Gestures
  def gestures(self, gesture_type):
    if gesture_type == Interact.GEST_MISSION_CONTROL:
      gesture_script = 'tell application "System Events" to key code 126 using control down'
    elif gesture_type == Interact.GEST_SWIPE_RIGHT:
      gesture_script = 'tell application "System Events" to key code 124 using control down'
    elif gesture_type == Interact.GEST_SWIPE_LEFT:
      gesture_script = 'tell application "System Events" to key code 123 using control down'
    elif gesture_type == Interact.GEST_APP_VIEW:
      gesture_script = 'tell application "System Events" to key code 125 using control down'
    # Snippet from https://github.com/dennisjanssen/PyLeapMouse/blob/f3da2214cd9698cbeffed32d3393f8a9a95d6c33/LeapFunctions.py#L92
    os.system("osascript -e '" + gesture_script + "'")
    self.gesture_timeout = Interact.GEST_TIMEOUT
