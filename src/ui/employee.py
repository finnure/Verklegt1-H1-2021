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
      'SEARCH_ID': self.__search_by_id_handler,
      'LIST_ALL': self.__list_all_handler,
      'VIEW': self.__view_employee_handler,
      'EDIT': self.__edit_employee_handler
    }

  def __menu_handler(self):
    ''' Displays Employee main menu and returns options and connections as a list'''
    menu = Menu(2, 6)
    menu.add_menu_item('I', 'SEARCH FOR A EMPLOYEE BY ID', 'EMPLOYEE:VIEW')
    menu.add_menu_item('A', 'VIEW ALL EMPLOYEES', 'EMPLOYEE:LIST_ALL')
    menu.add_menu_item('F', 'VIEW EMPLOYEES BY LOCATION', 'EMPLOYEE:SEARCH_LOCATION')
    menu.add_menu_item('R', 'GET REPORTS BY EMPLOYEE', 'EMPLOYEE:SEARCH_REPORTS')
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', 'EMPLOYEE:ADD_NEW')
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    self.__screen.display_menu(menu)
    return options

  def __view_employee_handler(self, id: int = 222):
    ''' Displays information about an employee with given id. '''
    emp = self.llapi.get_employee(id)
    if emp is None:
      self.__not_found_handler()
      return
    else:
      menu = Menu(12)
      menu.add_menu_item('T', 'VIEW USER TASKS', 'TASK:VIEW_FOR_EMPLOYEE')
      menu.add_menu_item('R', 'VIEW USER REPORTS', 'REPORT:VIEW_FOR_EMPLOYEE')
      options = menu.get_options()

      admin_menu = Menu(2, 13, 10)
      admin_menu.add_menu_item('/', 'EDIT', 'EMPLOYEES:EDIT')
      admin_menu.add_menu_item('+', 'ADD NEW', 'EMPLOYEES:ADD')
      options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
      
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
      self.__screen.print(emp.role, 8, 15)
      self.__screen.print('NUMBER OF ACTIVE TASKS: ', 10, 6, self.__screen.get_css_class('DATA_KEY'))
      self.__screen.print(str(self.llapi.get_active_tasks_for_user(emp.id)))

      self.__screen.display_menu(menu)
      return options


  def __search_by_id_handler(self):
    options = self.__menu_handler()
    menu = Menu(8, 15)
    menu.add_menu_item('1', 'LOCATION', 'LOCATION:EMPLOYEE_FILTER')
    menu.add_menu_item('2', 'SPECIALITY', 'EMPLOYEE:LIST_VIEW')
    self.__screen.print('FILTER BY:', 7, 15, self.__screen.get_css_class('DATA_KEY'))
    self.__screen.display_menu(menu)
    options.update(menu.get_options())
    return options

  def __list_all_handler(self):
    pass

  def __new_employee_handler(self):
    pass

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
    