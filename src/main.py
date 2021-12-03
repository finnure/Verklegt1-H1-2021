import sys
from uihandler import UiHandler


def main():
  ui = UiHandler()
  error = None
  try:
    ui.start()
  except Exception as err:
    error = err
  finally:
    ui.quit()
  if error is not None:
    print(error)



if __name__ == '__main__':
  main()