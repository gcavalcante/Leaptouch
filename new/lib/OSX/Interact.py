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

  def __init__(self):
    self.screen_width, self.screen_height = [(screen.frame().size.width, screen.frame().size.height) for screen in AppKit.NSScreen.screens()][-1]
    self.left_button_pressed = False
    self.mouse_x = 0
    self.mouse_y = 0
    self.last_mouse_state = False
	
  def update(self, finger_x, finger_y, pressed, fingers):
    if not hasattr(self, 'last'):
      self.last = (finger_x,finger_y,pressed,fingers)
    if fingers == 1:
      self.set_left_button_pressed(pressed)
    elif fingers == 2 and self.last[3] == 2:
      Interact.execute_event(CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitPixel, 2, self.last[1]-finger_y, self.last[0]-finger_x))
    elif fingers >= 3 and self.last[3] >= 3:
      if self.last[1] - finger_y > 60:
        Interact.gestures(Interact.GEST_MISSION_CONTROL)
      elif finger_y - self.last[1] > 60:
        Interact.gestures(Interact.GEST_MISSION_CONTROL)
      elif self.last[0] - finger_x > 60:
        Interact.gestures(Interact.GEST_SWIPE_RIGHT)
      elif finger_x - self.last[0] > 60:
        Interact.gestures(Interact.GEST_SWIPE_LEFT)

    self.move_mouse(finger_x, finger_y)
    self.last = (finger_x,finger_y,pressed,fingers)


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
  @staticmethod
  def gestures(gesture_type):
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
