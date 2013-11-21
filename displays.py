import platform

# Usage: Displays.resolutions() -> [(x1, y1), (x2, y2)]
class Displays(object):

  # OS Names
  OS_NAME_OSX = 'darwin'
  OS_NAME_WIN = '??'

  @staticmethod
  def resolutions():
    os_name = platform.system().lower()
    # OSX
    if os_name == Displays.OS_NAME_OSX:
      import AppKit
      return [(screen.frame().size.width, screen.frame().size.height) for screen in AppKit.NSScreen.screens()]
    # WIN
    elif os_name == Displays.OS_NAME_WIN:
      # TODO TEST THIS ON WINDOWS!
      import ctypes
      user32 = ctypes.windll.user32
      return (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
