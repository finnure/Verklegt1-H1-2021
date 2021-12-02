from uihandler import UiHandler


def main():
  ui = UiHandler()
  try:
    ui.start()
  except:
    pass
  ui.quit()



if __name__ == '__main__':
  main()