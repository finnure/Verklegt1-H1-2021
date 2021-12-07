from llapi import LlApi
from models.task import Task
from ui.screen import Screen
from models.building import Building
from ui.form import Form
from ui.table import Table
from ui.menu import Menu
from utils import Filters
from ui.constants import AccConst, BuildConst, LocConst, ReportConst, Styles, TaskConst

class ReportView():

  def __init__(self, screen: Screen, llapi: LlApi):
    self.__screen = screen
    self.llapi = llapi
    self.__create_input_map()

  def __create_input_map(self):
    ''' Dictionary with second half of menu item connection as key and
    handler method for that selection as value. '''
    self.__input_map = {
      #'LIST_ALL': self.__list_all_handler,
      'PAGING_NEXT': self.__paging_next_handler,
      'PAGING_PREV': self.__paging_prev_handler,
      'SELECT_FROM_LIST': self.__select_from_list_handler,
      #'VIEW': self.__view_handler,
      #'ADD_NEW': self.__add_new_handler,
      #'SAVE': self.__save_handler,
      #'GET_ID': self.__get_id_handler,
      'FILTER_TASK': self.__filter_task_handler,
      #'FILTER_EMPLOYEE': self.__filter_employee_handler,
      #'FILTER_CONTRACTOR': self.__filter_contractor_handler,
      #'FILTER_BUILDING': self.__filter_building_handler,
    }

  def find_handler(self, input: str):
    ''' This method is called by ui handler when an Building view is requested.
    The screen is cleared before calling the requested handler and refreshed
    before returning back to ui handler to make sure everything is displayed correctly. '''
    if input not in self.__input_map:
      raise KeyError(f'Building does not have a handler for {input}')
    handler: function = self.__input_map[input]
    self.__screen.clear()
    options = handler()
    self.__screen.refresh()
    return options

  def __paging_next_handler(self):
    ''' Go to next page of building list. If table is not available
    in params, list all handler will be called and whole list from page 
    one will be displayed. '''
    try:
      # pop table from params, go to next page and call list all handler with table
      table: Table = self.llapi.get_param(ReportConst.TABLE_PARAM)
      connection: str = self.llapi.get_param(ReportConst.CONNECTION_PARAM)
      table.next_page()
      # Return table back to params and return connection to list handler
      self.llapi.set_param(ReportConst.TABLE_PARAM, table)
      return connection
    except KeyError as err:
      self.__screen.print(str(err), 6, 6, 'ERROR')
      return {}

  def __paging_prev_handler(self):
    ''' Go to previous page of building list. If table is not available
    in params, list all handler will be called and whole list from page 
    one will be displayed. '''
    try:
      # pop table from params, go to next page and call list all handler with table
      table: Table = self.llapi.get_param(ReportConst.TABLE_PARAM)
      connection: str = self.llapi.get_param(ReportConst.CONNECTION_PARAM)
      table.previous_page()
      # Return table back to params and return connection to list handler
      self.llapi.set_param(ReportConst.TABLE_PARAM, table)
      return connection
    except KeyError as err:
      self.__screen.print(str(err), 6, 6, 'ERROR')
      return {}

  def __filter_task_handler(self):
    ''' Handler that gets a list of all Buildings and displays as a table.
    If too many rows are to be displayed, paging is applied.'''

    # Get task from params
    try:
      task: Task = self.llapi.get_param(TaskConst.TASK_PARAM)
    except KeyError as err:
      self.__screen.print(str(err), 6, 6, 'ERROR')

    reports = self.llapi.get_reports_for_task(task.id)
    table = Table(reports, ReportConst.TABLE_HEADERS)

    # Create and display menu option that allows user to select an item from the list
    menu = Menu()
    menu.add_menu_item('V', 'SELECT REPORT TO VIEW', ReportConst.SELECT_FROM_LIST)
    self.__screen.display_menu(menu)

    # Display the table and get paging options
    paging_options = self.__screen.display_table(table)
    if 'N' in paging_options:
      menu.add_menu_item('N', 'NEXT', ReportConst.PAGING_NEXT)
    if 'P' in paging_options:
      menu.add_menu_item('P', 'PREVIOUS', ReportConst.PAGING_PREV)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', BuildConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu,self.llapi.user.role))
    
    self.llapi.set_param(ReportConst.TABLE_PARAM, table)
    self.llapi.set_param(ReportConst.CONNECTION_PARAM, ReportConst.FILTER_TASK)

    return options


  def __select_from_list_handler(self):
    ''' Handler that allows user to select an Building from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    try:
      # Get table from params if available
      table: Table = self.llapi.get_param(BuildConst.TABLE_PARAM)
    except KeyError:
      # Else create a new table
      buildings = self.llapi.get_all_buildings()
      if len(buildings) <= 0:
        self.__screen.print('NO BUILDINGS FOUND', 5, 6, 'ERROR')
        return {}
      table = self.__create_table(buildings)
    
    self.__screen.print('ENTER NUMBER (#) OF BUILDING TO VIEW', 3, 6, Styles.DATA_KEY)
    while True: # Ask user to select Building
      filter = Filters.NUMBERS
      filter += self.__screen.display_table(table)
      selection = self.__screen.get_string(3, 43, 2, filter)
      # Clear error and previous input if exists
      [self.__screen.delete_character(3, x + 43) for x in range(40)]
      try:
        # Get selected Building and send it to View handler
        row = int(selection)
        building: Building = table.data[row - 1]
        self.__screen.clear() # Clears screen so view gets a clean canvas
        return self.__view_handler(building)
      except IndexError:
        # User should select a correct number, display error and try again
        self.__screen.print('INVALID NUMBER', 3, 60, Styles.ERROR)
      except ValueError:
        # Switching pages
        key = selection.upper()
        if key == 'P':
          table.previous_page()
        elif key == 'N':
          table.next_page()
        else:
          # Fat fingers, should only press either P or N and then Enter
          self.__screen.flash()


  def __create_table(self, tasks: 'list[Building]', begin_line: int = 5) -> Table:
    ''' Create a Table object from a list of Buildings. Table class takes in
    a list of building instances and list of headers to create a table. '''
    headers = {
      'id': 'ID',
      'address': 'ADDRESS',
      'location_id': 'LOCATION',
      'type': 'TYPE',
      'rooms': 'ROOMS',
      'state': 'STATE',
      'size': 'TASKS'
    }
    return Table(tasks, headers, begin_line)
