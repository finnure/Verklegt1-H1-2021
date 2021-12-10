from uihandler import UiHandler


def main():
  ui = UiHandler()
  error = None
  try:
    while ui.start():
      # If start returns true, user logged out, should call start again to login again
      pass
  except Exception as err:
    error = err
  finally:
    ui.quit()
  if error is not None:
    raise error



if __name__ == '__main__':
  main()