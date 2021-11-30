from uihandler import UiHandler


def main():
  ui = UiHandler()
  try:
    ui.login_view.display_view()
    user = ui.login_view.get_input()
    ui.view_frame.print_view()
    user = ui.login_view.get_input()
  except:
    pass
  ui.quit()
  print(user)





if __name__ == '__main__':
  main()