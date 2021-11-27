import curses
import os
import string
import utils
from typing import Tuple

class Screen():

  def __init__(self, lines: int = 42, cols: int = 122, 
               main: bool = True, begin_y: int = 0, begin_x: int = 0):
    ''' Creates an instance of screen that is used to display UI.
    By default, this is the complete program view.
    If main is set to False, a new sub-window is created and positioned
    using supplied properties '''
    self.lines = lines
    self.cols = cols
    self.__main = main
    self.set_default_commands()
    self.set_string_termination()
    if main:
      self.__init_main()
    else:
      self.__init_sub_window(lines, cols, begin_y, begin_x)

  def __init_main(self) -> None:
    ''' Creates the main window and initializes default settings '''
    self.__screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    self.__screen.keypad(True)

  def __init_sub_window(self, lines: int, cols: int, begin_y: int, begin_x: int) -> None:
    ''' Creates a sub window that is inside the main window '''
    self.__screen = curses.newwin(lines, cols, begin_y, begin_x)

  def set_default_commands(self, commands: list = None) -> None:
    ''' Sets default commands that are available anywhere. 
    If no list is sent as parameter, hardcoded defaults are used '''
    commands = utils.none_if_not_list(commands)
    if commands is None:
      self.default_commands = [
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
    else:
      self.default_commands = commands
  
  def set_string_termination(self, termination: list = None) -> None:
    ''' Sets default string termination for string inputs. 
    If no list is is sent as parameter, sane defaults are used '''
    termination = utils.none_if_not_list(termination)
    if termination is not None:
      self.string_termination = [
        ord('\t'), # TAB
        ord('\n'), # NEW LINE
        ord('\r'), # CARRIAGE RETURN
        curses.KEY_UP,
        curses.KEY_DOWN
      ]
    else:
      self.string_termination = termination

  def resize(self) -> bool:
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
    return terminal_size.lines == self.lines and terminal_size.columns == self.cols

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

  def get_string(self, filter: str = string.printable) -> str:
    ''' Collects input from keyboard and returns as string.
    Only printable characters are allowed by default.
    Terminates on Enter, Tab, Arrow up, Arrow down.
    Backspace removes character from list. 
    Arrow left and right change index '''
    # Turn on echo to make input appear in UI and curs_set True to make cursor visible
    curses.echo()
    curses.curs_set(True)
    accumulated_string = []
    index = 0
    while True:
      character = self.get_character()
      if character in self.string_termination:
        # break out of while loop to make sure echo is turned off again and cursor hidden
        break
      elif character == '127': # backspace
        if index > 0:
          index -= 1
          accumulated_string.pop(index)
          self.move_cursor_by_offset(0,-1)
        else:
          # Trying to delete from before string starts, need to move cursor back
          pass
      elif character == curses.KEY_LEFT and index > 0:
        index -= 1
        self.move_cursor_by_offset(0,-1)
      elif character == curses.KEY_RIGHT and index < len(accumulated_string):
        index += 1
        self.move_cursor_by_offset(0,1)
      elif chr(character) in filter:
        accumulated_string.insert(index, chr(character))
        index += 1
    # Reset terminal settings, hide cursor and input
    curses.noecho()
    curses.curs_set(False)
    # Return list as string
    return ''.join(accumulated_string)

  def __is_in_bounds(self, line: int, col: int) -> bool:
    ''' Checks if supplied coordinates are inside the screen area. 
    Return True if they are, else False '''
    if line < 0 or col < 0:
      return False
    if line > self.lines or col > self.cols:
      return False
    return True

  def __get_safe_coords(self, new_y: int, new_x: int, 
                      min_y: int = 1, min_x: int = 1,
                      max_y: int = 119, max_x: int = 119) -> Tuple[int, int] :
    ''' Checks if new coords are in-bounds. 
    If not, return safe coords that are inside min and max.
    y is lines and x is cols '''
    if not min_y <= new_y <= max_y:
      # new_y is out of bounds
      new_y = min_y if min_y < new_y else max_y
    if not min_x <= new_x <= max_x:
      new_x = min_x if min_x < new_x else max_x
    if self.__is_in_bounds(new_y, new_x):
      return (new_y, new_x)
    else:
      # someone fucked up, return top left corner to avoid throwing an error
      return (0,0)

  def __get_current_pos(self) -> Tuple[int,int]:
    ''' Gets current position of cursor and returns as tuple (line, col) '''
    return self.__screen.getyx()

  def move_cursor_by_offset(self, lines: int, cols: int) -> bool:
    ''' Moves cursor by offset specified by lines and cols.
    If movement goes out of bounds, it is set to in-bounds. '''
    if lines == 0 and cols == 0:
      # Nothing to move
      return False
    current_line, current_col = self.__get_current_pos()
    if not self.__is_in_bounds(current_line + lines, current_col + cols):
      # New position is out of bounds, return false
      return
    self.__screen.move(current_line + lines, current_col + cols)

  def move_cursor_to_coords(self, line: int, col: int,
                            min_y: int = 1, min_x: int = 1,
                            max_y: int = 119, max_x: int = 119) -> None:
    ''' Moves cursor to new coords. If trying to move out of bounds
    coords are updated to make sure an error is not thrown. '''
    new_line, new_col = self.__get_safe_coords(line, col, min_y, min_x, max_y, max_x)
    self.__screen.move(new_line, new_col)
  
  def end(self):
    curses.nocbreak()
    curses.echo()
    self.__screen.keypad(False)
    curses.endwin()
