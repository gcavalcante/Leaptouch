import Listener

def on_frame(point):
  print point
  pass


def main():
  listener = Listener.Listener(on_frame)
  foo = raw_input()

if __name__ == "__main__":
  main()
