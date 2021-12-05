from llapi import LlApi
from ui.constants import BuildConst, EmpConst, ReportConst, TaskConst
from ui.menu import Menu
from ui.screen import Screen

class SearchView():

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
    ''' This method is called by ui handler when the Search view is requested.
    The screen is cleared before calling the requested handler and refreshed
    before returning back to ui handler to make sure everything is displayed correctly. '''
    if input not in self.__input_map:
      raise KeyError(f'Search does not have a handler for {input}')
    handler: function = self.__input_map[input]
    self.__screen.clear()
    options = handler()
    self.__screen.refresh()
    return options
  

  def __menu_handler(self):
      ''' Displays main menu and returns options for it. '''
      # Create the main menu and get options as dict
      menu = Menu(9) # Menu starts in line 9
      menu.add_menu_item('1', 'SEARCH FOR EMPLOYEES BY CITY', EmpConst.FILTER_LOCATION)
      menu.add_menu_item('2', 'SEARCH FOR BUILDINGS BY CITY', BuildConst.FILTER_LOCATION)
      menu.add_menu_item('3', 'SEARCH FOR EMPLOYEE BY ID', EmpConst.GET_ID)
      menu.add_menu_item('4', 'SEARCH FOR BUILDING BY ID ', BuildConst.GET_ID)
      menu.add_menu_item('5', 'SEARCH FOR TASK BY ID', TaskConst.GET_ID)
      menu.add_menu_item('6', 'SEARCH FOR TASK BY BUILDINGS', TaskConst.FILTER_BUILDING)
      menu.add_menu_item('7', 'SEARCH FOR TASK BY EMPLOYEE', TaskConst.FILTER_EMPLOYEE)
      menu.add_menu_item('8', 'SEARCH FOR REPORTS BY CONTRACTOR', ReportConst.FILTER_CONTRACTOR)
      menu.add_menu_item('9', 'SEARCH FOR REPORT BY EMPLOYEE', ReportConst.FILTER_EMPLOYEE)
      options = menu.get_options()
      self.__screen.display_menu(menu)

      # Display header text using css class PAGE_HEADER
      self.__screen.print('SYSTEM SEARCH', 2, 50, 'PAGE_HEADER') # starting from line 2, col 40

      # Return options to uihandler
      return options


