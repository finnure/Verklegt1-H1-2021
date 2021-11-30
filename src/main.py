from uihandler import UiHandler
import locale


def main():
  locale.setlocale(locale.LC_ALL, '')
  ui = UiHandler()
  ui.login_view.display_view()
  user = ui.login_view.get_input()
  ui.quit()





if __name__ == '__main__':
  main()