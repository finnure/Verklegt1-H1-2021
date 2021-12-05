from llapi import LlApi
from ui.constants import BuildConst, ContrConst, EmpConst, LocConst, ReportConst, SearchConst, TaskConst
from ui.menu import Menu
from ui.screen import Screen


class MainMenuView():

  def __init__(self, screen: Screen, llapi: LlApi):
    self.__screen = screen
    self.llapi = llapi
    self.__create_input_map()

  def __create_input_map(self):
    ''' Dictionary with second half of menu item connection as key and
    handler method for that selection as value. '''
    self.__input_map = {
      'MENU': self.__menu_handler
    }

  def find_handler(self, input: str):
    ''' This method is called by ui handler when the MainMenu view is requested.
    The screen is cleared before calling the requested handler and refreshed
    before returning back to ui handler to make sure everything is displayed correctly. '''
    if input not in self.__input_map:
      raise KeyError(f'Employee does not have a handler for {input}')
    handler: function = self.__input_map[input]
    self.__screen.clear()
    options = handler()
    self.__screen.refresh()
    return options

  def __menu_handler(self):
    ''' Displays main menu and returns options for it. '''
    # Create the main menu and get options as dict
    menu = Menu(9) # Menu starts in line 9
    menu.add_menu_item('L', 'VIEW LOCATIONS', LocConst.MENU)
    menu.add_menu_item('B', 'VIEW BUILDINGS', BuildConst.MENU)
    menu.add_menu_item('E', 'VIEW EMPLOYEES', EmpConst.MENU)
    menu.add_menu_item('T', 'VIEW TASKS', TaskConst.MENU)
    menu.add_menu_item('C', 'VIEW CONTRACTORS', ContrConst.MENU)
    menu.add_menu_item('S', 'SEARCH', SearchConst.MENU)
    options = menu.get_options()
    self.__screen.display_menu(menu)

    # Create admin menu, displayed in top right corner
    admin_menu = Menu(2, 20) # Menu starts in line 2, options are 20 cols from right edge
    admin_menu.add_menu_item('+', 'CREATE NEW TASK', TaskConst.ADMIN_NEW)
    admin_menu.add_menu_item('R', 'ACTIVE REPORTS', ReportConst.ADMIN_ACTIVE)
    # Display admin menu if user role is MANAGER, and update options with displayed admin options
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))

    # Display header text using css class PAGE_HEADER
    self.__screen.print('WELCOME TO NAN AIR', 2, 50, 'PAGE_HEADER') # starting from line 2, col 40
    self.__screen.print('WHERE DIVISION BY ZERO MAKES SENSE!', 3, 40, 'PAGE_HEADER') # line 3 col 30

    # display greeting with logged in user name using css class DATA_KEY
    self.__screen.print(f'GOOD DAY {self.llapi.user.name}!', 6, 6, 'DATA_KEY') # line 6, col 6
    self.__screen.print('WHAT WOULD YOU LIKE TO DO TODAY?', 7, 6, 'DATA_KEY') # line 7, col 6

    # Return options to uihandler
    return options
