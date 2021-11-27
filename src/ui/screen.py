import curses
import os
import string
import utils
from typing import Tuple

class Screen():

  ########### INITIALIZATION #############

  def __init__(self, lines: int = 42, cols: int = 122,
               begin_y: int = 0, begin_x: int = 0,
               main: bool = False, border: bool = False):
    ''' Creates an instance of screen that is used to display UI sections.
    By default, a sub-window is created and positioned using supplied properties. 
    If border=True, a border is drawn around window and a new derived window
    created inside the border to make sure border is not overwritten by text.\n
    On program start, main=True needs to be passed to create the program window correctly.
    border, begin_y and begin_x are not used if main is True.
     '''
    self.lines = lines
    self.cols = cols
    self.__main = main
    self.__border = border
    self.set_default_commands()
    self.set_string_termination()
    if main:
      self.__init_main()
    else:
      self.__init_sub_window(lines, cols, begin_y, begin_x, border)

  def __init_main(self) -> None:
    ''' Creates the main window, initializes default settings and sets the size '''
    self.__screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    self.__screen.keypad(True)
    if curses.has_colors():
      curses.start_color()
    if not self.__resize():
      # Window is not big enough, kill with fire
      self.end()
      raise RuntimeError('Unable to resize terminal window. \
            Please switch to a supported terminal or set the \
            size manually to at least 42 lines and 122 columns and try again')

  def __init_sub_window(self, lines: int, cols: int, begin_y: int, begin_x: int, border: bool = False) -> None:
    ''' Creates a sub window that is inside the main window. 
    If border is True, border is drawn around the window and
    a derived window created inside the border. Size needs to
    be larger than 2x2 for border to be applied. '''
    screen = curses.newwin(lines, cols, begin_y, begin_x)
    if border and lines > 2 and cols > 2:
      screen.border()
      self.border_win = screen
      screen = screen.derwin(lines - 2, cols - 2, 1, 1)
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
    curses.resizeterm(self.lines, self.cols)
    return self.__window_size_correct()

  def __window_size_correct(self) -> bool:
    ''' Checks if terminal window size is of expected size
    Returns True if it is, False if it's not '''
    terminal_size = os.get_terminal_size()
    return terminal_size.lines >= self.lines and terminal_size.columns >= self.cols

  ######### PUBLIC METHODS ################

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

  def get_character(self, filter: list = None, default: bool = False) -> int:
    ''' Listenes to keyboard input and returns character.
    filter should be a list of available inputs.
    If default is true, default commands will be included'''
    filter = utils.none_if_not_list(filter)
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

  def get_string(self, cols: int = 64, filter: str = string.printable) -> str:
    ''' Collects input from keyboard and returns as string.
    Only printable characters are allowed by default.
    Terminates on Enter, Tab, Arrow up, Arrow down.
    Backspace removes character from list. 
    Arrow left and right change index.'''
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
        if index > 0:
          index -= 1
          accumulated_string.pop(index)
          self.move_cursor_by_offset(0,-1)
      elif character == curses.KEY_LEFT and index > 0:
        index -= 1
        self.move_cursor_by_offset(0,-1)
      elif character == curses.KEY_RIGHT and index < len(accumulated_string):
        index += 1
        self.move_cursor_by_offset(0,1)
      elif chr(character) in filter:
        accumulated_string.insert(index, chr(character))
        index += 1
      if len(accumulated_string) >= cols:
        # max string length reached, break out of while and return string
        break
    # Reset terminal settings, hide cursor and input
    curses.noecho()
    curses.curs_set(0)
    # Return list as string
    return ''.join(accumulated_string)

  def get_multiline_string(self, lines: int = 1, cols: int = 64, filter: string = string.printable) -> str:
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

  def print(self, text: str, line: int = None, col: int = None, style: int = 0):
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

  def delete_character(self, line: int, col: int) -> None:
    ''' Deletes character at specified position. 
    Checks if position is in-bounds first'''
    if self.__is_in_bounds(line, col):
      self.__screen.delch(line, col)

  def delete_line(self, line: int = None) -> None:
    ''' Delete line. Deletes current line if line is None, 
    otherwise moves to line and deletes it.
    This method is not permitted in main window '''
    if not self.__main:
      if line is not None and self.__is_in_bounds(line, 0):
        self.__screen.move(line, 0)
        self.__screen.deleteln()

  def flash(self) -> None:
    ''' Flashes the screen, reverses video for a short time.
    Can be used as a visible bell if user needs to be notified'''
    curses.flash()

  def end(self):
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

