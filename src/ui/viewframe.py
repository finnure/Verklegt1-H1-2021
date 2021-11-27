from .screen import Screen

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

  def __init__(self):
    self.__screen = Screen(main=True)
    self.__screen.set_color_pair(1, 122)
    self.display_frame()
    self.display_header()
    self.display_footer()

  def get_input(self):
    char = self.__screen.get_character()
    self.__screen.print(chr(char), 10,10)

  def display_frame(self):
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


  def display_header(self) -> None:
    ''' Displays header in window '''
    titles = ['(L)ocations', '(B)uilding', '(E)mployee', '(T)asks', '(C)ontractors', '(S)earch']
    dividers = [30, 46, 61, 76, 89, 107]
    top_line = 0
    self.__draw_divider_line(top_line + 4)
    self.__draw_sections(dividers, titles, top_line)

  def display_footer(self) -> None:
    ''' Displays footer in window '''
    titles = ['Log (O)ut', '(Q)uit']
    dividers = [95, 109]
    top_line = 36
    self.__draw_divider_line(top_line)
    self.__draw_sections(dividers, titles, top_line)


  def __draw_divider_line(self, line: int) -> None:
    ''' Draws a line across the complete window and replaces sides with side dividers '''
    max_col = self.__screen.cols - 2
    self.__screen.print(TOP_AND_BOTTOM * (max_col - 1), line, 1)
    self.__screen.print(LEFT_DIVIDER, line, 0)
    self.__screen.print(RIGHT_DIVIDER, line, max_col)

  def __draw_sections(self, start_list: list, title_list: list, from_line: int) -> None:
    ''' Divides header and footer into sections and displays on screen '''
    for i, col in enumerate(start_list):
      self.__screen.print(TOP_DIVIDER, from_line, col)
      self.__screen.print(BOTTOM_DIVIDER, from_line + 4, col)
      self.__screen.print(title_list[i], from_line + 2, col + 3, self.__header_style())
      for line in [from_line + 1, from_line + 2, from_line + 3]:
        self.__screen.print(SIDE, line, col)


  def __header_style(self) -> int:
    ''' Style of header text is defined here '''
    return self.__screen.get_style(['BOLD']) + self.__screen.get_color_pair(1)
