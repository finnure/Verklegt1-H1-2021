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

  def __display_admin_menu(self, menu: Menu) -> dict:
    ''' Displays a menu on the right side of the window if logged in user is manager. 
    Menu option is left justified and menu name is right justified. 
    Returns menu options if user is manager, else an empty dict. '''
    if self.llapi.user.role == 'MANAGER':
      max_col = self.__screen.cols
      for line, item in enumerate(menu):
        self.__screen.print(item.option + ' :', menu.start_line + line, max_col - menu.start_col) # Bæta við option style
        self.__screen.print(item.name, menu.start_line + line, max_col - menu.spacing)
      return menu.get_options()
    else:
      return {}

  def __display_menu(self, menu: Menu):
    ''' Displays a menu on the right side of the window. 
    Menu option is left justified and menu name is right justified. '''
    for line, item in enumerate(menu):
      self.__screen.print(item.option + ' :', menu.start_line + line, menu.start_col) # Bæta við option style
      self.__screen.print(item.name, menu.start_line + line, menu.start_col + menu.spacing)

  def __menu_handler(self):
    ''' Displays Employee main menu and returns options and connections as a list'''
    menu = Menu(2, 2)
    menu.add_menu_item('J', 'SEARCH FOR A EMPLOYEE BY ID', 'EMPLOYEE:SEARCH_ID')
    menu.add_menu_item('A', 'VIEW ALL EMPLOYEES', 'EMPLOYEE:LIST_ALL')
    menu.add_menu_item('F', 'VIEW EMPLOYEES BY LOCATION', 'EMPLOYEE:SEARCH_LOCATION')
    menu.add_menu_item('R', 'GET REPORTS BY EMPLOYEE', 'EMPLOYEE:SEARCH_REPORTS')
    options = menu.get_options()

    admin_menu = Menu(2, 15, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', 'EMPLOYEE:ADD_NEW')
    options.update(self.__display_admin_menu(admin_menu))
    self.__display_menu(menu)
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

      admin_menu = Menu(spacing=7)
      admin_menu.add_menu_item('E', 'EDIT', 'EMPLOYEES:EDIT')
      admin_menu.add_menu_item('+', 'ADD NEW', 'EMPLOYEES:ADD')
      options.update(self.__display_admin_menu(admin_menu))
      
      left_column = Menu(spacing=10)
      left_column.add_menu_item('NAME', emp.name)
      left_column.add_menu_item('PHONE', emp.phone)
      left_column.add_menu_item('MOBILE', emp.mobile)
      left_column.add_menu_item('EMAIL', emp.email)
      self.__display_menu(left_column)

      right_column = Menu(col=46, spacing=10)
      right_column.add_menu_item('ID', emp.id)
      right_column.add_menu_item('SSN', emp.ssn)
      right_column.add_menu_item('COUNTRY', emp.location_id)
      right_column.add_menu_item('ADDRESS', emp.address)
      self.__display_menu(right_column)

      self.__screen.print('ROLE:', 8, 5) # option style
      self.__screen.print(emp.role, 8, 14)
      self.__screen.print('NUMBER OF ACTIVE TASKS: ', 10, 5) # option style
      self.__screen.print(self.llapi.get_active_tasks_for_user(emp.id))

      self.__display_menu(menu)
      return options


  def __search_by_id_handler(self):
    pass

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
    