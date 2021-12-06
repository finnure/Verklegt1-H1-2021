from llapi import LlApi
from ui.menu import Menu
from ui.screen import Screen
from ui.constants import Styles

TOP_AND_BOTTOM = '\U00002500'
SIDE = '\U00002502'
TOP_DIVIDER = '\U0000252c'
BOTTOM_DIVIDER = '\U00002534'
TOP_LEFT_CORNER = '\U0000250c'
TOP_RIGHT_CORNER = '\U00002510'
BOTTOM_LEFT_CORNER ='\U00002514'
BOTTOM_RIGHT_CORNER ='\U00002518'
LEFT_DIVIDER = '\U0000251c'
RIGHT_DIVIDER = '\U00002524'

class ViewFrame():

  def __init__(self, screen: Screen, llapi: LlApi, header_menu: Menu, footer_menu: Menu):
    self.__screen = screen
    self.llapi = llapi
    self.header_menu = header_menu
    self.footer_menu = footer_menu

  def print_view(self):
    ''' Displays frame, header and footer on the screen. '''
    self.__screen.clear()
    self.__display_frame()
    self.__display_logo()
    self.__display_header()
    self.__display_footer()
    self.__display_logged_in_user()
    self.__screen.refresh()

  def __display_frame(self):
    ''' Draws the frame around the complete window '''
    max_line = self.__screen.lines - 2
    max_col = self.__screen.cols - 2
    # Top and bottom lines
    self.__screen.print(TOP_AND_BOTTOM * (max_col - 1), 0, 1)
    self.__screen.print(TOP_AND_BOTTOM * (max_col - 1), max_line, 1)
    # Left and right edges
    for line in range(1, max_line):
      self.__screen.print(SIDE, line, 0)
      self.__screen.print(SIDE, line, max_col)
    # Corners
    self.__screen.print(TOP_LEFT_CORNER, 0, 0)
    self.__screen.print(TOP_RIGHT_CORNER, 0, max_col)
    self.__screen.print(BOTTOM_LEFT_CORNER, max_line, 0)
    self.__screen.print(BOTTOM_RIGHT_CORNER, max_line, max_col)

  def __display_logo(self) -> None:
    ''' Displays logo in window. '''
    self.__screen.print('NaN', 1, 2, Styles.LOGO_NAME)
    self.__screen.print('NaN', 3, 26, Styles.LOGO_NAME)
    self.__screen.print('We divide by zero', 2, 7, Styles.LOGO_TEXT)

  def __display_header(self) -> None:
    ''' Displays header in window. '''
    titles = [item.name for item in self.header_menu]
    dividers = self.__get_dividers(titles)
    top_line = 0
    self.__draw_divider_line(top_line + 4)
    self.__draw_sections(dividers, titles, top_line)

  def __display_footer(self) -> None:
    ''' Displays footer in window '''
    titles = [item.name for item in self.footer_menu]
    dividers = self.__get_dividers(titles)
    top_line = 36
    self.__draw_divider_line(top_line)
    self.__draw_sections(dividers, titles, top_line)

  def __display_logged_in_user(self) -> None:
    ''' Displays information about logged in user in bottom left corner. '''
    menu = Menu(37, 2, 11)
    menu.add_menu_item('NAME', self.llapi.user.name)
    menu.add_menu_item('LOCATION', str(self.llapi.user.location_city)) # TODO breyta í location
    menu.add_menu_item('ROLE', self.llapi.user.role)
    self.__screen.display_menu(menu, Styles.DATA_KEY)


  def __draw_divider_line(self, line: int) -> None:
    ''' Draws a line across the complete window and replaces sides with side dividers. '''
    max_col = self.__screen.cols - 2
    self.__screen.print(TOP_AND_BOTTOM * (max_col - 1), line, 1)
    self.__screen.print(LEFT_DIVIDER, line, 0)
    self.__screen.print(RIGHT_DIVIDER, line, max_col)

  def __draw_sections(self, start_list: list, title_list: list, from_line: int) -> None:
    ''' Divides header and footer into sections and displays on screen. '''
    for i, col in enumerate(start_list):
      self.__screen.print(TOP_DIVIDER, from_line, col)
      self.__screen.print(BOTTOM_DIVIDER, from_line + 4, col)
      self.__screen.print(title_list[i], from_line + 2, col + 3, Styles.FRAME_TEXT)
      self.__screen.paint_character(Styles.OPTION, from_line + 2, col + 4)
      for line in [from_line + 1, from_line + 2, from_line + 3]:
        self.__screen.print(SIDE, line, col)

  def __get_dividers(self, titles: 'list[str]') -> 'list[int]':
    ''' Creates a list with spacing for dividers in header and footer. '''
    widths = [len(title) + 5 for title in titles]
    next_div = self.__screen.cols - sum(widths) - 2
    divs = []
    for w in widths:
      divs.append(next_div)
      next_div += w
    return divs
