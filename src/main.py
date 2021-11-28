from ui.screen import Screen
from ui.viewframe import ViewFrame



def main():
  screen = Screen(main=True)
  # create llapi
  # show login screen and ask for userid
  ui = ViewFrame(screen)
  ui.display_frame()
  ui.display_header()
  ui.display_footer()
  ui.get_input()
  ui.get_input()
  ui.get_input()




if __name__ == '__main__':
  main()