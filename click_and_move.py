################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.        #
# Leap Motion proprietary and confidential. Not for distribution.       #
# Use subject to the terms of the Leap Motion SDK Agreement available at    #
# https://developer.leapmotion.com/sdk_agreement, or another agreement     #
# between Leap Motion and you, your company or other organization.       #
################################################################################

import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from displays import Displays
z_glob = 9999

calibration = {
  'TL' : [999,-999,0],
  'BL' : [999,999,0],
  'TR' : [-999,-999,0],
  'BR' : [-999,999,0]

}

go_live = False






from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
def mouseEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(
                    None, 
                    type, 
                    (posx,posy), 
                    kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)

def mousemove(posx,posy):
        mouseEvent(kCGEventMouseMoved, posx,posy);

def mouseclick(posx,posy):
        # uncomment this line if you want to force the mouse 
        # to MOVE to the click location first (I found it was not necessary).
        #mouseEvent(kCGEventMouseMoved, posx,posy);
        mouseEvent(kCGEventLeftMouseDown, posx,posy);
        mouseEvent(kCGEventLeftMouseUp, posx,posy);



















def leapnormalizedz(posx, posy, posz):
	if 0 > 1 :
		normz = -1
	else :
		normz = blebleble

#print(leaptoscreen(-411, 79))
#print(leaptoscreen(431, 981))
#print(leaptoscreen(-410, 80))
#print(leaptoscreen(430, 980))
#print(leaptoscreen(10, 530))



class SampleListener(Leap.Listener):


  def set_calibration(self):
    self.leaplm = calibration['TL'][0]
    self.leaprm = calibration['TR'][0]
    self.leapum = calibration['TL'][1]
    self.leapdm = calibration['BL'][1]
    self.monlm = 0
    self.monrm,self.mondm = Displays.resolutions()[-1]
    self.monum = 0
    self.leapw = ((self.leaprm - self.leaplm) / 2)
    self.leaph = ((self.leapum - self.leapdm) / 2)
    self.monw = ((self.monrm - self.monlm) / 2)
    self.monh = ((self.mondm - self.monum) / 2)
  
  def leaptoscreen(self,posx,posy):
  	if posx >= self.leaplm and posx <= self.leaprm :
  		monx = (posx - self.leaplm) * self.monw / self.leapw
  	else :
  		monx = -1
  	if posy >= self.leapdm and posy <= self.leapum :
  		mony = abs(posy - self.leapum) * self.monh / self.leaph
  	else :
  		mony = -1
  	return [monx, mony]









  def get_calibration(self,vector):
    global calibration
    global z_glob
    X,Y,Z = (0,1,2)
    #print type(vector)
    x,y,z = vector.x,vector.y,vector.z
    #For TL
    if x < calibration['TL'][X]:
      calibration ['TL'][X]  = x
    if y > calibration['TL'][Y]:
      calibration ['TL'][Y]  = y

    #For BL
    if x < calibration['BL'][X]:
      calibration ['BL'][X]  = x
    if y < calibration['BL'][Y]:
      calibration ['BL'][Y]  = y

    #For TR
    if x > calibration['TR'][X]:
      calibration ['TR'][X]  = x
    if y > calibration['TR'][Y]:
      calibration ['TR'][Y]  = y

    #For BR
    if x > calibration['BR'][X]:
      calibration ['BR'][X]  = x
    if y < calibration['BR'][Y]:
      calibration ['BR'][Y]  = y

    if z < z_glob:
      z_glob = z




  def on_init(self, controller):
    print "Initialized"

  def on_connect(self, controller):
    print "Connected"

    # Enable gestures
    #controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
    #controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
    #controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
    #controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

  def on_disconnect(self, controller):
    # Note: not dispatched when running in a debugger.
    print "Disconnected"

  def on_exit(self, controller):
    print "Exited"

  def on_frame(self, controller):
    global calibration
    global go_live
    # Get the most recent frame and report some basic information
    frame = controller.frame()

    print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

    if not frame.hands.is_empty:
      # Get the first hand
      hand = frame.hands[0]

      # Check if the hand has any fingers
      fingers = hand.fingers
      if not fingers.is_empty:
        # Calculate the hand's average finger tip position
        #avg_pos = Leap.Vector()
        z_most = [0,0,99999999]
        finger_id = None
        for finger in fingers:
          #print finger
          #print finger.length
          #:w
          #print dir(finger)
          if finger.tip_position[2] < z_most[2]:
           z_most = finger.tip_position
           finger_id = finger.id
          #avg_pos += finger.tip_position
        print 'GO-LIVE',go_live
        if not go_live:
          print finger_id
          print z_most
          self.get_calibration(z_most)
        else:
          self.set_calibration()
          x,y,z = z_most.x,z_most.y,z_most.z
          X,Y = self.leaptoscreen(x,y)
          print 'IN_reso'
          print X,',',Y
          if z < -180:
            mouseclick(X,Y)
          else:
            mousemove(X,Y)
          
        #avg_pos /= len(fingers)
        #print "Hand has %d fingers, average finger tip position: %s" % (
        #   len(fingers), avg_pos)

#      # Get the hand's sphere radius and palm position
#      print "Hand sphere radius: %f mm, palm position: %s" % (
#         hand.sphere_radius, hand.palm_position)
#
#      # Get the hand's normal vector and direction
#      normal = hand.palm_normal
#      direction = hand.direction
#
#      # Calculate the hand's pitch, roll, and yaw angles
#      print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
#        direction.pitch * Leap.RAD_TO_DEG,
#        normal.roll * Leap.RAD_TO_DEG,
#        direction.yaw * Leap.RAD_TO_DEG)
#
#      # Gestures
#      for gesture in frame.gestures():
#        if gesture.type == Leap.Gesture.TYPE_CIRCLE:
#          circle = CircleGesture(gesture)
#
#          # Determine clock direction using the angle between the pointable and the circle normal
#          if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
#            clockwiseness = "clockwise"
#          else:
#            clockwiseness = "counterclockwise"
#
#          # Calculate the angle swept since the last frame
#          swept_angle = 0
#          if circle.state != Leap.Gesture.STATE_START:
#            previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
#            swept_angle = (circle.progress - previous_update.progress) * 2 * Leap.PI
#
#          print "Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
#              gesture.id, self.state_string(gesture.state),
#              circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)
#
#        if gesture.type == Leap.Gesture.TYPE_SWIPE:
#          swipe = SwipeGesture(gesture)
#          print "Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
#              gesture.id, self.state_string(gesture.state),
#              swipe.position, swipe.direction, swipe.speed)
#
#        if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
#          keytap = KeyTapGesture(gesture)
#          print "Key Tap id: %d, %s, position: %s, direction: %s" % (
#              gesture.id, self.state_string(gesture.state),
#              keytap.position, keytap.direction )
#
#        if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
#          screentap = ScreenTapGesture(gesture)
#          print "Screen Tap id: %d, %s, position: %s, direction: %s" % (
#              gesture.id, self.state_string(gesture.state),
#              screentap.position, screentap.direction )
#
    if not (frame.hands.is_empty and frame.gestures().is_empty):
      print ""

  def state_string(self, state):
    if state == Leap.Gesture.STATE_START:
      return "STATE_START"

    if state == Leap.Gesture.STATE_UPDATE:
      return "STATE_UPDATE"

    if state == Leap.Gesture.STATE_STOP:
      return "STATE_STOP"

    if state == Leap.Gesture.STATE_INVALID:
      return "STATE_INVALID"

def main():
  global go_live
  # Create a sample listener and controller
  listener = SampleListener()
  controller = Leap.Controller()

  # Have the sample listener receive events from the controller
  controller.add_listener(listener)

  # Keep this process running until Enter is pressed
  print "Press Enter to quit..."
  sys.stdin.readline()
  print calibration
  go_live = True
  sys.stdin.readline()
  # Remove the sample listener when done
  controller.remove_listener(listener)


if __name__ == "__main__":
  main()
