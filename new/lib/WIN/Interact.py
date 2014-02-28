import ctypes
from ctypes import c_int
      
# WIN interaction class
class Interact():

  def __init__(self):
    user32 = ctypes.windll.user32
    self.screen_width, self.screen_height = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    self.left_button_pressed = False
    self.mouse_x = 0
    self.mouse_y = 0
    self.last_mouse_state = False
    self.buffer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
    #elif fingers == 2 and self.last[3] == 2:
    #  ctypes.windll.user32.mouse_event(2, c_int(int(round(self.mouse_x))), c_int(int(round(self.mouse_y))), c_int(int(round(finger_y-self.last[1]))), 0)
    
    self.move_mouse(finger_x, finger_y)
    self.last = (finger_x,finger_y,pressed,fingers)
    self.addtobuffer(finger_x,finger_y,pressed,fingers)


  def move_mouse(self, x, y):
    self.mouse_x = x
    self.mouse_y = y
    self.check_and_correct_borders();
    if self.left_button_pressed: # Drag!
      ctypes.windll.user32.SetCursorPos(c_int(int(round(self.mouse_x))), c_int(int(round(self.mouse_y))))
      #Interact.execute_event(CGEventCreateMouseEvent(None, kCGEventLeftMouseDragged, (), 0))
    else: # Just move
      ctypes.windll.user32.SetCursorPos(c_int(int(round(self.mouse_x))), c_int(int(round(self.mouse_y))))

  def set_left_button_pressed(self, boolean_button): 
    if boolean_button == True and not self.last_mouse_state:
      self.click_down()
    elif not boolean_button and self.last_mouse_state: 
      self.click_up()
    self.last_mouse_state = boolean_button
        
  def click_down(self):
    ctypes.windll.user32.mouse_event(2, c_int(int(round(self.mouse_x))), c_int(int(round(self.mouse_y))), 0, 0)
    self.left_button_pressed = True

  def click_up(self):
    ctypes.windll.user32.mouse_event(4, c_int(int(round(self.mouse_x))), c_int(int(round(self.mouse_y))), 0, 0)
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
