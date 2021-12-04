from models.employee import Employee
from ui.form import Form
from ui.table import Table
import utils
from llapi import LlApi
from ui.screen import Screen
from ui.menu import Menu

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
      'ADD_NEW': self.__new_employee_handler,
      'FILTER_LOCATION': self.__filter_location_handler,
      'LIST_ALL': self.__list_all_handler,
      'SELECT_FROM_LIST': self.__select_from_list_handler,
      'VIEW': self.__view_employee_handler,
      'EDIT': self.__edit_employee_handler,
      'GET_ID': self.__get_id_handler
    }


  ################## Handler methods #########################

  def __menu_handler(self):
    ''' Displays Employee main menu and returns options and connections as a list'''
    menu = Menu(2, 6)
    menu.add_menu_item('I', 'SEARCH FOR A EMPLOYEE BY ID', 'EMPLOYEE:GET_ID')
    menu.add_menu_item('A', 'VIEW ALL EMPLOYEES', 'EMPLOYEE:LIST_ALL')
    menu.add_menu_item('F', 'VIEW EMPLOYEES BY LOCATION', 'EMPLOYEE:FILTER_LOCATION')
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', 'EMPLOYEE:ADD_NEW')
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    self.__screen.display_menu(menu)
    return options

  def __view_employee_handler(self, emp: 'int | Employee'):
    ''' Displays information about an employee with given id. '''
    if type(emp) is int:
      emp = self.llapi.get_employee(input)
      # taka þetta út ef verður ekki notað, annars klára villumeðhöndlun

    menu = Menu(12)
    menu.add_menu_item('T', 'VIEW USER TASKS', 'TASK:VIEW_FOR_EMPLOYEE')
    menu.add_menu_item('R', 'VIEW USER REPORTS', 'REPORT:VIEW_FOR_EMPLOYEE')
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('/', 'EDIT', 'EMPLOYEES:EDIT')
    admin_menu.add_menu_item('+', 'ADD NEW', 'EMPLOYEES:ADD')
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    
    self.__display_one_employee(emp)
    self.__screen.display_menu(menu)
    return options

  def __filter_location_handler(self):
    options = self.__menu_handler()
    return options

  def __get_id_handler(self):
    ''' Ask user to enter id of employee to find. '''
    options = self.__menu_handler()
    self.__screen.print('PLEASE ENTER ID:', 8, 10)
    employee_id = self.__screen.get_string(8, 28, 3, utils.NUMBERS)
    emp = self.llapi.get_employee(int(employee_id))
    if emp is None:
      self.__screen.print(f'NO EMPLOYEE FOUND WITH ID {employee_id}', 10, 10, self.__screen.get_css_class('ERROR'))
      self.__screen.print('PRESS I TO SEARCH AGAIN', 11, 10)
      self.__screen.paint_character(self.__screen.get_css_class('OPTION'), 11, 16)
      return options
    # Employee found, clear screen and display info
    self.__screen.clear()
    self.__view_employee_handler(emp)

  def __list_all_handler(self):
    emps = self.llapi.get_all_employees()
    table = self.__create_table(emps)
    menu = Menu()
    menu.add_menu_item('V', 'SELECT AN EMPLOYEE TO VIEW', 'EMPLOYEE:SELECT_FROM_LIST')
    options = menu.get_options()
    self.__screen.display_menu(menu)

    admin_menu = Menu()
    admin_menu.add_menu_item('+', 'ADD NEW', 'EMPLOYEE:ADD_NEW')
    options.update(self.__screen.display_admin_menu(admin_menu,self.llapi.user.role))
    
    self.__screen.display_table(table)
    return options

  def __select_from_list_handler(self):
    emps = self.llapi.get_all_employees()
    self.__screen.print('ENTER NUMBER (#) OF EMPLOYEE TO VIEW', 3, 6, self.__screen.get_css_class('DATA_KEY'))
    table = self.__create_table(emps)
    while True:
      filter = utils.NUMBERS
      filter += self.__screen.display_table(table)
      selection = self.__screen.get_string(3, 43, 2, filter)
      [self.__screen.delete_character(3, x + 43) for x in range(40)]
      try:
        row = int(selection)
        emp = emps[row - 1]
        self.__screen.clear()
        return self.__view_employee_handler(emp)
      except IndexError:
        self.__screen.print('INVALID NUMBER', 3, 60, self.__screen.get_css_class('ERROR'))
      except ValueError:
        key = selection.upper()
        if key == 'F':
          table.first_page()
        elif key == 'P':
          table.previous_page()
        elif key == 'N':
          table.next_page()
        elif key == 'L':
          table.last_page()
        else:
          self.__screen.flash()

  def __new_employee_handler(self):
    self.__screen.refresh()
    form = Form(Employee.get_new_fields())
    form_window = self.__screen.display_form(form)
    for field in form:
      form_window.edit_form_field(field)
    return ''

  def __edit_employee_handler(self, id: int):
    pass

  def __not_found_handler(self):
    pass

  def find_handler(self, input: str, params = None):
    if input not in self.__input_map:
      raise KeyError(f'Employee does not have a handler for {input}')
    handler: function = self.__input_map[input]
    self.__screen.clear()
    options = handler(params) if params is not None else handler()
    self.__screen.refresh()
    return options


  ########## Display data methods ##################


  def __display_one_employee(self, emp: Employee) -> None:
    left_column = Menu(spacing=10)
    left_column.add_menu_item('NAME', emp.name)
    left_column.add_menu_item('PHONE', emp.phone)
    left_column.add_menu_item('MOBILE', emp.mobile)
    left_column.add_menu_item('EMAIL', emp.email)
    self.__screen.display_menu(left_column, 'DATA_KEY')

    right_column = Menu(3, 46, 10)
    right_column.add_menu_item('ID', str(emp.id))
    right_column.add_menu_item('SSN', emp.ssn)
    right_column.add_menu_item('COUNTRY', str(emp.location_id))
    right_column.add_menu_item('ADDRESS', emp.address)
    self.__screen.display_menu(right_column, 'DATA_KEY')

    self.__screen.print('ROLE', 8, 6, self.__screen.get_css_class('DATA_KEY'))
    self.__screen.print(emp.role, 8, 16)
    self.__screen.print('NUMBER OF ACTIVE TASKS: ', 10, 6, self.__screen.get_css_class('DATA_KEY'))
    self.__screen.print(str(self.llapi.get_active_tasks_for_user(emp.id)))

  def __create_table(self, emps: Table, begin_line: int = 5) -> Table:
    headers = {
      'id': 'ID',
      'name': 'NAME',
      'phone': 'CITY',
      'mobile': 'MOBILE',
      'email': 'EMAIL'
    }
    return Table(emps, headers, begin_line)

