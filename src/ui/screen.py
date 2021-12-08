import curses
import os
from models.employee import Employee
from ui.form import Form, FormField
from ui.menu import Menu
from ui.table import Table
import utils
from utils import Filters
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
    self.begin_y = begin_y
    self.begin_x = begin_x
    self.__parent = parent
    self.__border = border
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
    self.__screen.keypad(False)
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
    screen = self.__parent.create_sub_window(self.lines, self.cols, begin_y, begin_x)
    if self.__border and self.lines > 2 and self.cols > 2:
      screen.border()
      self.border_win = screen
      screen = screen.derwin(self.lines - 2, self.cols - 2, 1, 1)
    self.color_supported = self.__parent.color_supported
    self.max_color_pairs = self.__parent.max_color_pairs
    self.max_colors = self.__parent.max_colors
    self.__screen = screen

  def __resize(self) -> bool:
    ''' Tries to resize terminal window
    Detects operating system and sends the correct terminal command
    Returns True if resize was successfull, False otherwise '''
    if self.__parent is not None:
      # Not allowed to resize sub-window
      return False
    if self.__window_size_correct():
      # Window is of correct size, return True and do nothing
      return True
    if os.name == 'posix': # Linux or Mac
      os.system(f'printf "\e[8;{self.lines};{self.cols}t"')
    else:
      os.system(f'mode con: cols={self.cols} lines={self.lines}')
    sleep(0.01) # Need to give OS a chance to finish resize before checking if successful
    return self.__window_size_correct()

  def __window_size_correct(self) -> bool:
    ''' Checks if terminal window size is of expected size
    Returns True if it is, False if it's not '''
    terminal_size = os.get_terminal_size()
    return terminal_size.lines >= self.lines and terminal_size.columns >= self.cols

  ######### PUBLIC METHODS ################

  ######### Color and style methods ############

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

  def get_css_class(self, name: str) -> int:
    ''' Returns a pre-defined "css class" for it to be applied to text in the view.
    Available css classes:\n
    ERROR, FRAME_TEXT, OPTION, LOGO_NAME, LOGO_TEXT, TABLE_HEADER, PAGE_HEADER, DATA_KEY, DISABLED, EDITING
    '''
    css_classes: 'dict[str,tuple[int,list[str]]]' = {
      'ERROR': (1,['REVERSE']),
      'FRAME_TEXT': (2,['BOLD']),
      'OPTION': (3,['BOLD']),
      'LOGO_NAME': (4,['BOLD']),
      'LOGO_TEXT': (5,['BOLD']),
      'TABLE_HEADER': (6,['UNDERLINE']),
      'PAGE_HEADER': (7,['BOLD']),
      'DATA_KEY': (8,['BOLD']),
      'DISABLED': (9,['NORMAL']),
      'EDITING': (10, ['NORMAL'])
    }
    if name not in css_classes:
      return 0
    color, style = css_classes[name]
    return self.get_color_pair(color) + self.get_style(style)

  ################ UI display methods ####################

  def display_admin_menu(self, menu: Menu, role: str) -> dict:
    ''' Displays a menu on the right side of the window if logged in user is manager. 
    Menu option is left justified and menu name is right justified. 
    Returns menu options if user is manager, else an empty dict. '''
    if role == 'MANAGER':
      max_col = self.cols
      for line, item in enumerate(menu):
        self.print(item.option, menu.start_line + line, max_col - menu.start_col, self.get_css_class('OPTION'))
        self.print(item.name, menu.start_line + line, max_col - len(item.name) - 2)
      return menu.get_options()
    else:
      return {}

  def display_menu(self, menu: Menu, css_class: str = 'OPTION', role: str = None) -> None:
    ''' Displays a menu on the window positioned with settings on the class. '''
    line = 0
    for item in menu:
      if role is not None and item.role is not None and role != item.role:
        # logged in users role should not see this menu item
        continue
      self.print(item.option, menu.start_line + line, menu.start_col, self.get_css_class(css_class))
      self.print(item.name, menu.start_line + line, menu.start_col + menu.spacing)
      line += 1

  def display_table(self, table: Table) -> str:
    ''' Creates a new window for table and displays it. If paging is true, paging footer is also displayed.
    Returns paging options as a string. '''
    filter = ''
    lines = table.max_lines + 5
    window = Screen(lines, self.cols - table.begin_col - 2, table.begin_line, table.begin_col, False, self)
    window.clear()
    col = 0
    for column in table:
      window.print(column.name, 0, col, window.get_css_class('TABLE_HEADER'))
      for line, row in enumerate(column):
        window.print(str(row), line + 2, col)
      col += column.get_width()
    if table.pages > 0:
      filter = window.display_table_footer(table, table.max_lines + 3)
    window.refresh()
    return filter

  def display_table_footer(self, table: Table, line: int = 22) -> str:
    ''' Prints paging info for table and returns paging options as string. '''
    filter = ''
    total_rows = len(table.data)
    style = self.get_css_class('DATA_KEY')
    option_style = self.get_css_class('OPTION')
    disabled_style = self.get_css_class('DISABLED')

    self.print('TOTAL ROWS ', line, 0, style)
    self.print(str(total_rows))
    self.move_cursor_by_offset(0, 2)
    self.print('PAGE ', style=style)
    self.print(str(table.current_page + 1) + '/' + str(table.pages + 1))
    self.move_cursor_by_offset(0, 2)
    if table.current_page > 0:
      # Previous
      filter += 'Pp'
      self.print('P', line, 35, option_style)
      self.print('REVIOUS', style=style)
    # disabled Previous
    if table.current_page == 0:
      self.print('PREVIOUS', line, 35, disabled_style)
    # disabled Next
    if table.current_page == table.pages:
      self.print('NEXT', line, 50, disabled_style)
    # Next
    if table.current_page < table.pages:
      filter += 'Nn'
      self.print('N', line, 50, option_style)
      self.print('EXT ', style=style)
    return filter

  def select_from_table(self, table: Table, line, question_text):
    col = len(question_text) + 8
    self.print(question_text, line, 6, 'DATA_KEY')
    while True: # Ask user to select Location
      filter = Filters.NUMBERS
      filter += self.display_table(table)
      selection = self.get_string(line, col, 2, filter)
      # Clear error and previous input if exists
      self.delete_character(line, col, 116 - col)
      try:
        # Get selected Location
        row = int(selection)
        return table.data[row - 1]
      except IndexError:
        # User should select a correct number, display error and try again
        self.print('INVALID NUMBER', line, col + 5, 'ERROR')
      except ValueError:
        # Switching pages
        key = selection.upper()
        if key == 'P':
          table.previous_page()
        elif key == 'N':
          table.next_page()
        else:
          # Fat fingers, should only press either P or N and then Enter
          self.flash()


  def display_form(self, form: Form, begin_line: int = 8, begin_col: int = 6):
    ''' Creates a new window and displays the form on it. 
    Returns the new window to enable editing. '''
    lines = form.lines
    if self.lines < begin_line + lines:
      # Too many lines for parent window, fill to the bottom.
      lines = self.lines - begin_line
    if lines < 0:
      raise RuntimeError(f'Not enough lines in parent window. Parent lines: {self.lines}, required lines: {begin_line}')
    cols = self.cols - begin_col - 2 # use all available-2 columns in parent from begin_col
    
    window = Screen(lines, cols, begin_line, begin_col, False, self)
    window.clear()
    line = 0
    for field in form: # iterate over each form field and print on screen
      window.print(field.name, line, 0, window.get_css_class('DATA_KEY'))
      if field.value is not None:
        # Editing an already existing object. Display current values
        window.print(str(field.value), line, form.spacing)
      # Set starting position of field value for editing
      field.set_position(line, form.spacing)
      line += field.get_lines() # Supports multiline fields
    window.refresh() # Make all the stuff appear on screen
    return window

  def edit_form_field(self, field: FormField) -> str:
    ''' Allows user to edit field, mutates value. '''
    # Need to add extra column to sub window to make sure cursor doesn't go out of bounds on last char
    window = Screen(field.lines, field.cols + 1, field.line, field.col, parent=self)
    error_length = 0
    # Try until value is of correct format  
    while True:
      # Clear previous value from screen so get_string() gets a clear canvas.
      window.clear()
      window.refresh()
      # Make sure value is string or None before sending to get_string
      field_value = str(field.value) if field.value is not None else None
      value = window.get_string(0, 0, field.cols, field.filter, field_value, True)
      try:
        [validate(value) for validate in field.validators]
        self.delete_character(field.line, field.col + field.cols + 5, error_length)
        self.refresh()
        field.value = value
        break
      except ValueError as err:
        error_length = len(str(err))
        self.print(str(err), field.line, field.col + field.cols + 5, self.get_css_class('ERROR'))
        self.refresh()
      except TypeError:
        # Validator is not a function
        pass
    
    # Remove EDITING formatting 
    window.paint_character(0,0,0,field.cols)
    window.refresh()

  ############### Input/output #####################

  def set_string_termination(self, termination: list = None) -> None:
    ''' Sets default string termination for string inputs. 
    If no list is is sent as parameter, sane defaults are used '''
    termination = utils.none_if_not_list(termination)
    if termination is None:
      termination = [
        ord('\t'), # TAB
        ord('\n'), # NEW LINE
        ord('\r'), # CARRIAGE RETURN
        curses.KEY_UP,
        curses.KEY_DOWN,
        curses.KEY_ENTER
      ]
    self.string_termination = termination

  def get_character(self) -> str:
    ''' Listenes to keyboard input and returns character. '''
    return self.__screen.get_wch()

  def get_string(self, line: int, col: int, cols: int = 64, filter: str = Filters.ALL_PRINTABLE, value: str = None, editing: bool = False) -> str:
    ''' Collects input from keyboard and returns as string.
    Only printable characters are allowed by default.
    Terminates on Enter, Tab, Arrow up, Arrow down.
    Backspace removes character from list. '''
    # Make cursor visible and move it to start of line
    started_editing = False
    curses.curs_set(1)
    self.move_cursor_to_coords(line, col)
    accumulated_string = []
    index = 0
    if value is not None:
      # Editing a form field that already has value. Prepare values accordingly and display current value
      accumulated_string = list(value)
      index = len(accumulated_string)
      self.print(value)
    if editing:
      # Do fancy visual stuff to make the text we're editing stand out
      self.paint_character(self.get_css_class('EDITING'), line, col, cols)
      self.move_cursor_by_offset(0, index)
      self.refresh()
    while True:
      character = self.get_character()
      try:
        char = ord(character)
      except TypeError:
        char = char
      if char in self.string_termination:
        # break out of while loop to make sure echo is turned off again and cursor hidden
        break
      elif char in [8, 127, curses.KEY_BACKSPACE]: # backspace
        if index > 0: # Not possible to erase if cursor is at beginning of string
          # Move index back and pop character from accumulated string
          index -= 1
          accumulated_string.pop()
          # Move cursor back one space and delete character at position
          self.move_cursor_by_offset(0,-1)
          self.delete_character()
        else:
          self.flash()
      elif character in filter:
        # Add allowed character to string and move cursor and index
        accumulated_string.append(character)
        index += 1
        self.print(character)
      else:
        # Character not allowed
        self.flash()
        continue
      if editing:
        # Re-apply fancy visual stuff to keep looks consistent and move cursor to correct position
        self.paint_character(self.get_css_class('EDITING'), line, col, cols)
        self.move_cursor_by_offset(0, index)
        self.refresh()
        if not started_editing:
          # Give user a chance to delete from a string that is of max length
          started_editing = True
          continue
      if len(accumulated_string) >= cols:
        # max string length reached, break out of while and return string        
        break
    # Reset terminal settings, hide cursor
    curses.curs_set(0)
    # Return list as string
    return ''.join(accumulated_string)

  def get_multiline_string(self, lines: int = 1, cols: int = 64, filter: str = Filters.ALL_PRINTABLE) -> str:
    ''' Collects multiple lines and returns as one string. '''
    first_line, first_col = self.__get_current_pos()
    accumulated_lines = []
    for i in range(lines):
      self.move_cursor_to_coords(first_line + i, first_col)
      new_line = self.get_string(cols, filter)
      if len(new_line) == 0:
        # Empty line treated as input termination, break out of for loop and return string
        break
      elif len(new_line) != cols:
        # Enter key pressed, add newline character to string
        new_line += '\n'
      # Possible feature: move last part of new line to next line and replace with newline character.
      accumulated_lines.append(new_line)
    return ''.join(accumulated_lines)

  def print(self, text: str, line: int = None, col: int = None, style: 'int | str' = 0) -> None:
    ''' Prints text to screen. If line and col are not specified, 
    string will be printed at current cursor location.
    Style can be a number or the name of a css class. Available css classes are:
    ERROR, FRAME_TEXT, OPTION, LOGO_NAME, LOGO_TEXT, TABLE_HEADER, PAGE_HEADER, DATA_KEY, DISABLED, EDITING.
    Default style is white text on black background.  '''
    # Convert style to a number if it's a string, getting css class
    if type(style) is str:
      style = self.get_css_class(style)
    if line is None or col is None:
      # Need both to print text at location, using current location
      self.__screen.addstr(text, style)
    else:
      self.__screen.addstr(line, col, text, style)

  def horizontal_line(self, cols: int, line: int = None, col: int = None):
    ''' Displays a horizontal line on the screen starting at position line, col
    ranging cols character. If line or col is None, line will start at current cursor position'''
    if line is None or col is None:
      self.__screen.hline(curses.ACS_BSBS, cols)
    else:
      self.__screen.hline(line, col, curses.ACS_BSBS, cols)

  def print_selected(self, selected: bool, line: int, col: int):
    ''' Prints a green checkmark if selected is true, else a red x. '''
    CHECK = '\U00002713'
    CROSS = '\U00002716'
    text = CHECK if selected else CROSS
    color = 11 if selected else 12

    self.__screen.addstr(line, col, text, self.get_color_pair(color))



  #################### Utility methods #######################

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

  def paint_character(self, style: 'int | str', line: int = None,
                      col: int = None, num: int = 1) -> None:
    ''' Paints characters in the style given.
    If line and col are supplied, character at that position is painted, 
    else current position is used.
    Default number of characters painted is 1. If num is supplied 
    that number of characters will be painted from position specified 
    Style can be a number or the name of a css class. Available css classes are:
    ERROR, FRAME_TEXT, OPTION, LOGO_NAME, LOGO_TEXT, TABLE_HEADER, PAGE_HEADER, DATA_KEY, DISABLED, EDITING. '''
    if type(style) is str:
      style = self.get_css_class(style)
    if line is None or col is None:
      self.__screen.chgat(num, style)
    else:
      self.__screen.chgat(line, col, num, style)

  def delete_character(self, line: int = None, col: int = None, num: int = 1) -> None:
    ''' Deletes character at specified position, or current position if none specified
    Checks if position is in-bounds first'''
    # Delete one or more characters
    for _ in range(num):
      try:
        if line is None or col is None:
          # Delete characters from current position
          self.__screen.delch()
        else: 
          self.__screen.delch(line, col)
      except:
        # Ignore errors, most likely because position is out of bounds
        return

  def delete_line(self, line: Union[int, None] = None) -> None:
    ''' Delete line. Deletes current line if line is None, 
    otherwise moves to line and deletes it.
    This method is not permitted in main screen '''
    if self.__parent is not None:
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

  def flush_input(self) -> None:
    ''' Clears the input buffer if any keyboard input is waiting in buffer. '''
    curses.flushinp()

  def create_sub_window(self, lines: int, cols: int, begin_y: int, begin_x: int):
    ''' Creates a sub window starting at position begin_y x begin_x
    with the size of lines and cols. If specified size is too big
    for the parent window, sub window will range from begin_y x begin_x
    to the bottom right corner of the parent window. '''
    if begin_y + lines > self.lines or begin_x + cols > self.cols:
      return self.__screen.derwin(begin_y, begin_x)
    else:
      return self.__screen.derwin(lines, cols, begin_y, begin_x)

  def end(self) -> None:
    ''' If called on main window, everything is set to normal. 
    If called on a sub-window, that window is destroyed '''
    if self.__parent is None:
      curses.nocbreak()
      curses.echo()
      curses.curs_set(True)
      self.__screen.keypad(False)
      curses.endwin()

  ######### PRIVATE METHODS ################

  def __is_in_bounds(self, line: int, col: int) -> bool:
    ''' Checks if supplied coordinates are inside the screen area. 
    Return True if they are, else False '''
    if line < 0 or col < 0:
      return False
    if line >= self.lines or col >= self.cols:
      return False
    return True

  def __get_safe_coords(self, new_y: int, new_x: int) -> Tuple[int, int] :
    ''' Checks if new coords are in-bounds. 
    If not, return safe coords that are inside min and max.
    y is lines and x is cols '''
    if not 0 <= new_y <= self.lines:
      # new_y is out of bounds
      new_y = 0 if 0 < new_y else self.lines
    if not 0 <= new_x <= self.cols:
      new_x = 0 if 0 < new_x else self.cols
    if self.__is_in_bounds(new_y, new_x):
      return (new_y, new_x)
    else:
      # someone fucked up, return top left corner to avoid throwing an error
      return (0, 0)

  def __get_current_pos(self) -> Tuple[int,int]:
    ''' Gets current position of cursor and returns as tuple (line, col) '''
    return self.__screen.getyx()

