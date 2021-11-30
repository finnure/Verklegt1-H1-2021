import curses
from curses import _CursesWindow
import os
import utils
from typing import Tuple, Union
from time import sleep

class Screen():

  ########### INITIALIZATION #############

  def __init__(self, lines: int = 42, cols: int = 122,
               begin_y: int = 0, begin_x: int = 0,
               border: bool = False, parent: 'Screen' = None):
    ''' Creates an instance of screen that is used to display UI sections.
    By default, a sub-window is created and positioned using supplied properties. 
    If border=True, a border is drawn around window and a new derived window
    created inside the border to make sure border is not overwritten by text.\n
    On program start, main=True needs to be passed to create the program window correctly.
    border, begin_y and begin_x are not used if main is True.
     '''
    self.lines = lines
    self.cols = cols
    self.__parent = parent
    self.__border = border
    self.set_default_commands()
    self.set_string_termination()
    if self.__parent is None:
      self.__init_main()
    else:
      self.__init_sub_window(begin_y, begin_x)

  def __init_main(self) -> None:
    ''' Creates the main window, initializes default settings and sets the size '''
    if not self.__resize():
      # Window is not big enough, kill with fire
      raise RuntimeError('Wrong terminal size, needs to be at least 122x42. Please resize manually and try again')
    self.__screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    self.__screen.keypad(True)
    # Check if color is supported. Init color info if it is
    self.color_supported = curses.has_colors()
    if self.color_supported:
      curses.start_color()
      self.max_color_pairs = curses.COLOR_PAIRS
      self.max_colors = curses.COLORS

  def __init_sub_window(self, begin_y: int, begin_x: int) -> None:
    ''' Creates a sub window that is inside the main window. 
    If border is True, border is drawn around the window and
    a derived window created inside the border. Size needs to
    be larger than 2x2 for border to be applied. '''
    screen = self.__parent.create_sub_window(begin_y, begin_x)
    if self.__border and self.lines > 2 and self.cols > 2:
      screen.border()
      self.border_win = screen
      screen = screen.derwin(self.lines - 2, self.cols - 2, 1, 1)
    self.__screen = screen

  def __resize(self) -> bool:
    ''' Tries to resize terminal window
    Detects operating system and sends the correct terminal command
    Returns True if resize was successfull, False otherwise '''
    if not self.__main:
      # Not allowed to resize sub-window
      return False
    if self.__window_size_correct():
      # Window is of correct size, return True and do nothing
      return True
    if os.name == 'posix': # Linux or Mac
      os.system(f'printf "\e[8;{self.lines};{self.cols}t"')
    else:
      os.system(f'mode con: cols={self.cols} lines={self.lines}"')
    sleep(0.01) # Need to give OS a chance to finish resize before checking if successful
    return self.__window_size_correct()

  def __window_size_correct(self) -> bool:
    ''' Checks if terminal window size is of expected size
    Returns True if it is, False if it's not '''
    terminal_size = os.get_terminal_size()
    return terminal_size.lines >= self.lines and terminal_size.columns >= self.cols

  ######### PUBLIC METHODS ################

  def set_color_pair(self, pair: int, text_color: int, background_color: int = 0) -> None:
    ''' Defines color pair if color is supported and if numbers don't exceed max allowed. 
    Default background color is black.
    Each color should be a number representing that color. '''
    if not self.color_supported:
      # Do nothing if color is not supported
      return
    if text_color > self.max_colors or background_color > self.max_colors:
      # Do nothing if trying to use unsupported color
      return
    if pair > self.max_color_pairs:
      # Do nothing if trying to set unsupported color pair
      return
    curses.init_pair(pair, text_color, background_color)

  def get_color_pair(self, pair: int = 0) -> int:
    ''' Gets color pair. Returns 0 if color is not supported or pair is not supported. '''
    if self.color_supported and pair < self.max_color_pairs:
      return curses.color_pair(pair)
    else:
      return 0

  def get_style(self, style_list: list) -> int:
    ''' Get style from list of styles. Returns 0 if color is not supported.
    Supported styles: BOLD, UNDERLINE, REVERSE, BLINK.
    Each style has a number. To use multiple styles, sum of all styles is used. '''
    if not self.color_supported:
      return 0
    style_dict = {
      'BOLD': curses.A_BOLD,
      'UNDERLINE': curses.A_UNDERLINE,
      'REVERSE': curses.A_REVERSE,
      'BLINK': curses.A_BLINK
    }
    return sum([style_dict[style] for style in style_list if style in style_dict])

  def set_default_commands(self, commands: list = None) -> None:
    ''' Sets default commands that are available anywhere. 
    If no list is sent as parameter, hardcoded defaults are used '''
    commands = utils.none_if_not_list(commands)
    if commands is None:
      commands = [
        curses.KEY_F1,
        curses.KEY_F2,
        curses.KEY_F3,
        curses.KEY_F4,
        curses.KEY_F5,
        curses.KEY_F6,
        ord('q'),
        ord('Q'),
        ord('o'),
        ord('O'),
      ]
    self.default_commands = commands
  
  def set_string_termination(self, termination: list = None) -> None:
    ''' Sets default string termination for string inputs. 
    If no list is is sent as parameter, sane defaults are used '''
    termination = utils.none_if_not_list(termination)
    if termination is not None:
      termination = [
        ord('\t'), # TAB
        ord('\n'), # NEW LINE
        ord('\r'), # CARRIAGE RETURN
        curses.KEY_UP,
        curses.KEY_DOWN
      ]
    self.string_termination = termination

  def get_character(self, filter: Union[list, str, None] = None, default: bool = False) -> int:
    ''' Listenes to keyboard input and returns character.
    filter should be a list of available inputs.
    If default is true, default commands will be included'''
    if type(filter) is not None:
      # Convert to a list of ascii numbers with both upper and lowercase
      filter = utils.get_ascii_list(filter)
    if type(filter) is list and default:
      # Append default commands to filter
      filter.extend(self.default_commands)
    while True:
      character = self.__screen.getch()
      if filter is None and not default:
        # No filters specified, return any key
        return character
      elif filter is None and character in self.default_commands:
        # Only default commands are returned
        return character
      elif filter is not None and character in filter:
        # Filter is set, only return key if it's in filter list
        return character

  def get_string(self, cols: int = 64, filter: str = utils.ALL_PRINTABLE) -> str:
    ''' Collects input from keyboard and returns as string.
    Only printable characters are allowed by default.
    Terminates on Enter, Tab, Arrow up, Arrow down.
    Backspace removes character from list. '''
    # Turn on echo to make input appear in UI and curs_set True to make cursor visible
    curses.echo()
    curses.curs_set(1)
    accumulated_string = []
    index = 0
    while True:
      character = self.get_character()
      if character in self.string_termination:
        # break out of while loop to make sure echo is turned off again and cursor hidden
        break
      elif character == curses.erasechar(): # backspace
        if index > 0: # Not possible to erase if cursor is at beginning of string
          # Move index back and pop character from accumulated string
          index -= 1
          accumulated_string.pop()
          # Move cursor back one space and delete character at position
          self.move_cursor_by_offset(0,-1)
          self.delete_character()
      elif chr(character) in filter:
        # Add allowed character to string and move cursor and index
        accumulated_string.append(chr(character))
        index += 1
        self.move_cursor_by_offset(0, 1)
      else:
        # Character not allowed
        self.flash()
      if len(accumulated_string) >= cols:
        # max string length reached, break out of while and return string
        break
    # Reset terminal settings, hide cursor and input
    curses.noecho()
    curses.curs_set(0)
    # Return list as string
    return ''.join(accumulated_string)

  def get_multiline_string(self, lines: int = 1, cols: int = 64, filter: str = utils.ALL_PRINTABLE) -> str:
    ''' Collects multiple lines and returns as one string concatenated by \\n '''
    first_line, first_col = self.__get_current_pos()
    accumulated_lines = []
    for i in range(lines):
      self.move_cursor_to_coords(first_line + i, first_col)
      next_line = self.get_string(cols, filter)
      if len(next_line) == 0:
        # Empty line treated as input termination, break out of for loop and return string
        break
      accumulated_lines.append(next_line)
    return '\n'.join(accumulated_lines)

  def print(self, text: str, line: int = None, col: int = None, style: int = 0) -> None:
    ''' Prints text to screen. If line and col are not specified, 
    string will be printed at current cursor location.
    Style should be a number computed by adding together color profile and effects.
    Default style is white text on black background '''
    if line is None or col is None:
      # Need both to print text at location
      self.__screen.addstr(text, style)
    else:
      self.__screen.addstr(line, col, text, style)

  def move_cursor_by_offset(self, lines: int, cols: int) -> bool:
    ''' Moves cursor by offset specified by lines and cols.
    If movement goes out of bounds, no movement is made and False returned. 
    If movement is safe, move is performed and True returned '''
    if lines == 0 and cols == 0:
      # Nothing to move
      return False
    current_line, current_col = self.__get_current_pos()
    if not self.__is_in_bounds(current_line + lines, current_col + cols):
      # New position is out of bounds, return false
      return False
    self.__screen.move(current_line + lines, current_col + cols)

  def move_cursor_to_coords(self, line: int, col: int) -> None:
    ''' Moves cursor to new coords. If trying to move out of bounds
    coords are updated to make sure an error is not thrown. '''
    new_line, new_col = self.__get_safe_coords(line, col)
    self.__screen.move(new_line, new_col)
  
  def clear(self) -> None:
    ''' Clears everything from the window '''
    self.__screen.clear()

  def refresh(self) -> None:
    ''' Updates the window and redraws it '''
    self.__screen.refresh()

  def paint_character(self, style: int, line: Union[int, None] = None,
                      col: Union[int, None] = None, num: int = 1) -> None:
    ''' Paints characters in the style given.
    If line and col are supplied, character at that position is painted, 
    else current position is used.
    Default number of characters painted is 1. If num is supplied 
    that number of characters will be painted from position specified '''
    if line is None or col is None:
      self.__screen.chgat(num, style)
    else:
      self.__screen.chgat(line, col, num, style)

  def delete_character(self, line: Union[int, None] = None, col: Union[int, None] = None) -> None:
    ''' Deletes character at specified position, or current position if none specified
    Checks if position is in-bounds first'''
    if line is None or col is None:
      self.__screen.delch()
    elif self.__is_in_bounds(line, col):
      self.__screen.delch(line, col)

  def delete_line(self, line: Union[int, None] = None) -> None:
    ''' Delete line. Deletes current line if line is None, 
    otherwise moves to line and deletes it.
    This method is not permitted in main screen '''
    if not self.__main:
      if line is not None and self.__is_in_bounds(line, 0):
        self.__screen.move(line, 0)
        self.__screen.deleteln()
      elif line is None:
        # delete current line
        self.__screen.deleteln()

  def flash(self) -> None:
    ''' Flashes the screen, reverses video for a short time.
    Can be used as a visible bell if user needs to be notified'''
    curses.flash()

  def create_sub_window(self, begin_y: int, begin_x: int) -> '_CursesWindow':
    ''' Creates a sub window starting at position begin_y x begin_x
    with the size of lines and cols. If specified size is too big
    for the parent window, sub window will range from begin_y x begin_x
    to the bottom right corner of the parent window. '''
    if begin_y + self.lines > self.__parent.lines or begin_x + self.cols > self.__parent.cols:
      return self.__screen.subwin(begin_y, begin_x)
    else:
      return self.__screen.subwin(self.lines, self.cols, begin_y, begin_x)

  def end(self) -> None:
    ''' If called on main window, everything is set to normal. 
    If called on a sub-window, that window is destroyed '''
    if self.__main:
      curses.nocbreak()
      curses.echo()
      curses.curs_set(True)
      self.__screen.keypad(False)
      curses.endwin()

  ######### PRIVATE METHODS ################

  def __is_in_bounds(self, line: int, col: int) -> bool:
    ''' Checks if supplied coordinates are inside the screen area. 
    Return True if they are, else False '''
    min_y, min_x = self.__screen.getbegyx()
    if line < min_y or col < min_x:
      return False
    if line >= self.lines or col >= self.cols:
      return False
    return True

  def __get_safe_coords(self, new_y: int, new_x: int) -> Tuple[int, int] :
    ''' Checks if new coords are in-bounds. 
    If not, return safe coords that are inside min and max.
    y is lines and x is cols '''
    min_y, min_x = self.__screen.getbegyx()
    if not min_y <= new_y <= self.lines:
      # new_y is out of bounds
      new_y = min_y if min_y < new_y else self.lines
    if not min_x <= new_x <= self.cols:
      new_x = min_x if min_x < new_x else self.cols
    if self.__is_in_bounds(new_y, new_x):
      return (new_y, new_x)
    else:
      # someone fucked up, return top left corner to avoid throwing an error
      return (min_y, min_x)

  def __get_current_pos(self) -> Tuple[int,int]:
    ''' Gets current position of cursor and returns as tuple (line, col) '''
    return self.__screen.getyx()

