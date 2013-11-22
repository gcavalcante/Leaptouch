import AppKit#, Leap, subprocess
from Quartz.CoreGraphics import (CGEventCreateMouseEvent,CGEventPost,CGDisplayBounds,
    CGEventCreateScrollWheelEvent,CGEventSourceCreate,kCGScrollEventUnitPixel,
    kCGScrollEventUnitLine,kCGEventMouseMoved,kCGEventLeftMouseDragged,
    kCGEventLeftMouseDown,kCGEventLeftMouseUp,kCGMouseButtonLeft,kCGEventRightMouseDown,
    kCGEventRightMouseDown,kCGEventRightMouseUp,kCGMouseButtonRight,kCGHIDEventTap)
#from Leap import SwipeGesture 

# OSX interaction class
class Interact():

  def __init__(self):
    self.screen_width, self.screen_height = [(screen.frame().size.width, screen.frame().size.height) for screen in AppKit.NSScreen.screens()][-1]
    self.left_button_pressed = False
    self.mouse_x = 0
    self.mouse_y = 0
    self.last_mouse_state = False
	
  def update(self, finger_x, finger_y, pressed, fingers):
    if fingers == 1:
      self.set_left_button_pressed(pressed)
    elif fingers == 2 and self.last[3] == 2:
      RelativeMouseScroll(self.last[0]-finger_x,self.last[1]-finger_y)
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

  def interact_power(fingers, gestures):
    for gesture in gestures:
      if gesture.type == Leap.Gesture.TYPE_SWIPE:
        swipe = SwipeGesture(gesture)
      # Snippet from https://github.com/dennisjanssen/PyLeapMouse/blob/f3da2214cd9698cbeffed32d3393f8a9a95d6c33/LeapFunctions.py#L92
      PIPE = subprocess.PIPE
      osa = subprocess.Popen('osascript', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
      (out, err) = osa.communicate(gesture_script)
      gesture_script = None


def RelativeMouseScroll(x_movement, y_movement):  #Movements should be no larger than +- 10
    scrollWheelEvent = CGEventCreateScrollWheelEvent(
            None,  #No source
            kCGScrollEventUnitPixel,  #We are using pixel units
            2,  #Number of wheels(dimensions)
            y_movement,
            x_movement)
    CGEventPost(kCGHIDEventTap, scrollWheelEvent)
