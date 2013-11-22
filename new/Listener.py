from lib import Leap
import sys

#INIT
N_FRAMES = 10


class Listener(Leap.Listener):

  def __init__(self,callback):
    super(Listener, self).__init__()
    self.callback = callback
    self.controller = Leap.Controller()
    self.controller.add_listener(self)
  def __del__(self):
    super(Listener, self).__del__()
    self.controller.remove_listener(self)

  def medium_z_last_frames(self,N,controler):
    #todo: look at click.py and do in a clear way
    pass

  def on_init(self, controller):
    print "Initialized"
  
  def on_connect(self, controller):
    print "Connected"

  def on_disconnect(self, controller):
    # Note: not dispatched when running in a debugger.
    print "Disconnected"

  def on_exit(self, controller):
    print "Exited"

  def on_frame(self, controller):
    frames = [controller.frame(i) for i in xrange(N_FRAMES)]
    frames.reverse()

    avg = [0, 0, 0]
    frame_count = 0

    for frame in frames:
      if frame.pointables.is_empty:
        continue
      if frame.pointables.frontmost is not None:
        p = frame.pointables.frontmost.tip_position
        avg[0] += p[0]
        avg[1] += p[1]
        avg[2] += p[2]

        frame_count += 1
    if frame_count == 0:
      self.callback(None)
    else:
      avg[0] /= frame_count
      avg[1] /= frame_count
      avg[2] /= frame_count
      self.callback(avg)


#Only to debug reasons
#def main():
#  global go_live
#  # Create a sample listener and controller
#  listener = Listener()
#  controller = Leap.Controller()
#
#  # Have the sample listener receive events from the controller
#  controller.add_listener(listener)
#
#  # Keep this process running until Enter is pressed
#  print "Press Enter to quit..."
#  sys.stdin.readline()
#  print calibration
#  go_live = True
#  sys.stdin.readline()
#  # Remove the sample listener when done
#  controller.remove_listener(listener)
#
#
#if __name__ == "__main__":
#  main()
