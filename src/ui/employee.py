from models.employee import Employee
from ui.form import Form
from ui.table import Table
from utils import Filters
from llapi import LlApi
from ui.screen import Screen
from ui.menu import Menu
from ui.constants import EmpConst, GlobalConst, Styles

class EmployeeView():

  def __init__(self, screen: Screen, llapi: LlApi):
    self.__screen = screen
    self.llapi = llapi
    self.__create_input_map()

  def __create_input_map(self):
    ''' Dictionary with second half of menu item connection as key and
    handler method for that selection as value. '''
    self.__input_map = {
      'MENU': self.__menu_handler,
      'FILTER_LOCATION': self.__filter_location_handler,
      'LIST_ALL': self.__list_all_handler,
      'LIST_ALL_NEXT': self.__list_all_paging_next_handler,
      'LIST_ALL_PREV': self.__list_all_paging_prev_handler,
      'LIST_TASKS': self.__list_tasks_handler,
      'LIST_REPORTS': self.__list_reports_handler,
      'SELECT_FROM_LIST': self.__select_from_list_handler,
      'VIEW': self.__view_employee_handler,
      'ADD_NEW': self.__new_employee_handler,
      'SAVE': self.__save_employee_handler,
      'EDIT': self.__edit_employee_handler,
      'GET_ID': self.__get_id_handler
    }


  ################## Handler methods #########################

  def __menu_handler(self):
    ''' Displays Employee main menu and returns options and connections as a list'''
    menu = Menu(2, 6)
    menu.add_menu_item('I', 'SEARCH FOR A EMPLOYEE BY ID', EmpConst.GET_ID)
    menu.add_menu_item('A', 'VIEW ALL EMPLOYEES', EmpConst.LIST_ALL)
    menu.add_menu_item('F', 'VIEW EMPLOYEES BY LOCATION', EmpConst.FILTER_LOCATION)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', EmpConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    self.__screen.display_menu(menu)
    return options

  def __view_employee_handler(self, emp: Employee):
    ''' Displays information about an employee. '''
    menu = Menu(12)
    menu.add_menu_item('T', 'VIEW USER TASKS', EmpConst.LIST_TASKS)
    menu.add_menu_item('R', 'VIEW USER REPORTS', EmpConst.LIST_REPORTS)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('/', 'EDIT', EmpConst.ADMIN_EDIT)
    admin_menu.add_menu_item('+', 'ADD NEW', EmpConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    
    self.__display_one_employee(emp)
    self.__screen.display_menu(menu)
    # Store emp in params so edit handler can pick it up and handle editing
    self.llapi.set_param(EmpConst.EMPLOYEE_PARAM, emp)
    return options

  def __filter_location_handler(self):
    options = self.__menu_handler()
    return options

  def __get_id_handler(self):
    ''' Ask user to enter id of employee to find. '''
    options = self.__menu_handler()
    self.__screen.print('PLEASE ENTER ID:', 8, 10)
    employee_id = self.__screen.get_string(8, 28, 3, Filters.NUMBERS)
    emp = self.llapi.get_employee(int(employee_id))
    if emp is None:
      self.__screen.print(f'NO EMPLOYEE FOUND WITH ID {employee_id}', 10, 10, Styles.ERROR)
      self.__screen.print('PRESS I TO SEARCH AGAIN', 11, 10)
      self.__screen.paint_character('OPTION', 11, 16)
      return options
    # Employee found, clear screen and call view handler to display info
    self.__screen.clear()
    return self.__view_employee_handler(emp)

  def __list_all_paging_next_handler(self):
    ''' Go to next page of employee list. If table is not available
    in params, list all handler will be called and whole list from page 
    one will be displayed. '''
    try:
      # pop table from params, go to next page and call list all handler with table
      table: Table = self.llapi.get_param(EmpConst.TABLE_PARAM)
      table.next_page()
      return self.__list_all_handler(table)
    except KeyError:
      return self.__list_all_handler()

  def __list_all_paging_prev_handler(self):
    ''' Go to previous page of employee list. If table is not available
    in params, list all handler will be called and whole list from page 
    one will be displayed. '''
    try:
      # pop table from params, go to previous page and call list all handler with table
      table: Table = self.llapi.get_param(EmpConst.TABLE_PARAM)
      table.previous_page()
      return self.__list_all_handler(table)
    except KeyError:
      return self.__list_all_handler()

  def __list_all_handler(self, table: Table = None):
    ''' Handler that gets a list of all Employees and displays as a table.
    If too many rows are to be displayed, paging is applied.'''
    if table is None:
      # First call to list. If table is not None, paging is being used
      emps = self.llapi.get_all_employees()
      table = self.__create_table(emps)

    # Create and display menu option that allows user to select an item from the list
    menu = Menu()
    menu.add_menu_item('V', 'SELECT AN EMPLOYEE TO VIEW', EmpConst.SELECT_FROM_LIST)
    self.__screen.display_menu(menu)

    # Display the table and get paging options
    paging_options = self.__screen.display_table(table)
    if 'N' in paging_options:
      menu.add_menu_item('N', 'NEXT', EmpConst.LIST_ALL_NEXT)
    if 'P' in paging_options:
      menu.add_menu_item('P', 'PREVIOUS', EmpConst.LIST_ALL_PREV)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', EmpConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu,self.llapi.user.role))
    
    if table.pages > 0:
      # Store table so paging handlers can use paging
      self.llapi.set_param(EmpConst.TABLE_PARAM, table)

    return options

  def __list_tasks_handler(self):
    pass

  def __list_reports_handler(self):
    pass

  def __select_from_list_handler(self):
    ''' Handler that allows user to select an Employee from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    try:
      # Get table from params if available
      table: Table = self.llapi.get_param(EmpConst.TABLE_PARAM)
    except KeyError:
      # Else create a new table
      emps = self.llapi.get_all_employees()
      table = self.__create_table(emps)
    
    self.__screen.print('ENTER NUMBER (#) OF EMPLOYEE TO VIEW', 3, 6, Styles.DATA_KEY)
    while True: # Ask user to select Employee
      filter = Filters.NUMBERS
      filter += self.__screen.display_table(table)
      selection = self.__screen.get_string(3, 43, 2, filter)
      # Clear error and previous input if exists
      [self.__screen.delete_character(3, x + 43) for x in range(40)]
      try:
        # Get selected Employee and send it to View handler
        row = int(selection)
        emp: Employee = table.data[row - 1]
        self.__screen.clear() # Clears screen so view gets a clean canvas
        return self.__view_employee_handler(emp)
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

  def __new_employee_handler(self):
    ''' Handler to display a form to enter data for new Employee. '''
    self.__screen.print('CREATE NEW EMPLOYEE', 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE FILL THE FORM TO CREATE A NEW EMPLOYEE', 5, 6, Styles.DATA_KEY)
    self.__screen.refresh()
    form = Form(Employee.get_new_fields())
    form_window = self.__screen.display_form(form)
    for field in form:
      if field.options is not None:
        # TODO Display options list
        pass
      if field.editable:
        form_window.edit_form_field(field)
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(EmpConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(18)
    menu.add_menu_item('A', 'APPLY CHANGES', EmpConst.SAVE)
    menu.add_menu_item('D', 'DISCARD CHANGES', EmpConst.MENU)
    self.__screen.display_menu(menu)
    return menu.get_options()

  def __save_employee_handler(self):
    ''' After adding new or editing an employee, this handler will save to disk
    if user chooses to apply changes. '''
    try:
      form: Form = self.llapi.get_param(EmpConst.FORM_PARAM)
    except KeyError as err:
      # This really shouldn't happen. We'll put this here anyways.
      self.__screen.print(str(err), 6, 6, Styles.ERROR)
      return {}
    emp = self.llapi.new_employee(form)
    return self.__view_employee_handler(emp)

  def __edit_employee_handler(self):
    ''' Handler to display a form to edit Employee. '''
    try:
      emp = self.llapi.get_param(EmpConst.EMPLOYEE_PARAM)
    except KeyError as err:
      self.__screen.print(str(err), 6, 6, Styles.ERROR)
    return {}


  def find_handler(self, input: str):
    ''' This method is called by ui handler when an Employee view is requested.
    The screen is cleared before calling the requested handler and refreshed
    before returning back to ui handler to make sure everything is displayed correctly. '''
    if input not in self.__input_map:
      raise KeyError(f'Employee does not have a handler for {input}')
    handler: function = self.__input_map[input]
    self.__screen.clear()
    options = handler()
    self.__screen.refresh()
    return options



  def __display_one_employee(self, emp: Employee) -> None:
    ''' Displays information about an employee on the screen. '''
    left_column = Menu(spacing=10)
    left_column.add_menu_item('NAME', emp.name)
    left_column.add_menu_item('PHONE', emp.phone)
    left_column.add_menu_item('MOBILE', emp.mobile)
    left_column.add_menu_item('EMAIL', emp.email)
    self.__screen.display_menu(left_column, Styles.DATA_KEY)

    right_column = Menu(3, 46, 10)
    right_column.add_menu_item('ID', str(emp.id))
    right_column.add_menu_item('SSN', emp.ssn)
    right_column.add_menu_item('COUNTRY', str(emp.location_id))
    right_column.add_menu_item('ADDRESS', emp.address)
    self.__screen.display_menu(right_column, Styles.DATA_KEY)

    self.__screen.print('ROLE', 8, 6, Styles.DATA_KEY)
    self.__screen.print(emp.role, 8, 16)
    self.__screen.print('NUMBER OF ACTIVE TASKS: ', 10, 6, Styles.DATA_KEY)
    self.__screen.print(str(self.llapi.get_active_tasks_for_user(emp.id)))

  def __create_table(self, emps: 'list[Employee]', begin_line: int = 5) -> Table:
    ''' Create a Table object from a list of Employees. Table class takes in
    a list of employee instances and list of headers to create a table. '''
    headers = {
      'id': 'ID',
      'name': 'NAME',
      'phone': 'CITY',
      'mobile': 'MOBILE',
      'email': 'EMAIL'
    }
    return Table(emps, headers, begin_line)

