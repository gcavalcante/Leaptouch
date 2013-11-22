
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
from Quartz.CoreGraphics import (CGEventCreateMouseEvent,CGEventPost,CGDisplayBounds,
    CGEventCreateScrollWheelEvent,CGEventSourceCreate,kCGScrollEventUnitPixel,
    kCGScrollEventUnitLine,kCGEventMouseMoved,kCGEventLeftMouseDragged,
    kCGEventLeftMouseDown,kCGEventLeftMouseUp,kCGMouseButtonLeft,kCGEventRightMouseDown,
    kCGEventRightMouseDown,kCGEventRightMouseUp,kCGMouseButtonRight,kCGHIDEventTap)



class Interact():
  def mouseEvent(self,type, posx, posy):
          theEvent = CGEventCreateMouseEvent(
                      None, 
                      type, 
                      (posx,posy), 
                      kCGMouseButtonLeft)
          CGEventPost(kCGHIDEventTap, theEvent)
  
  def mousemove(self,posx,posy):
          self.mouseEvent(kCGEventMouseMoved, posx,posy);
  
  def mousedown(self,posx,posy):
    print 'MOUSE DOWN ', posx, posy
    # uncomment this line if you want to force the mouse 
    # to MOVE to the click location first (I found it was not necessary).
    #mouseEvent(kCGEventMouseMoved, posx,posy);
    self.mouseEvent(kCGEventLeftMouseDown, posx,posy);
  
  def mouseup(self,posx,posy):
    print 'MOUSE UP ', posx, posy
    self.mouseEvent(kCGEventLeftMouseUp, posx,posy);
  
  def mousedragEvent(self,posx,posy):
    print 'MOUSE DRAG ', posx, posy
    self.mouseEvent(kCGEventLeftMouseDragged, posx,posy);
