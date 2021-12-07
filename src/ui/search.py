from llapi import LlApi
from models.employee import Employee
from models.location import Location
from ui.constants import BuildConst, EmpConst, LocConst, ReportConst, SearchConst, Styles, TaskConst
from ui.menu import Menu
from ui.screen import Screen
from ui.table import Table
from utils import Filters

class SearchView():

  def __init__(self, screen: Screen, llapi: LlApi):
    self.__screen = screen
    self.llapi = llapi
    self.__create_input_map()
  
  def __create_input_map(self):
    ''' Dictionary with second half of menu item connection as key and
    handler method for that selection as value. '''
    self.__input_map = {
      'MENU': self.__menu_handler,
      'EMPLOYEE_BY_LOCATION': self.__emp_by_location_handler,
      'BUILDING_BY_LOCATION': self.__build_by_location_handler,
      'EMPLOYEE_BY_ID': self.__emp_by_id_handler,
      'BUILDING_BY_ID': self.__build_by_id_handler,
      'TASK_BY_ID': self.__task_by_id_handler,
      'TASK_BY_BUILDING': self.__task_by_building_handler,
      'TASK_BY_EMPLOYEE': self.__task_by_emp_handler,
      'REPORT_BY_BUILDING': self.__report_by_build_handler,
      'REPORT_BY_EMPLOYEE': self.__report_by_emp_handler,
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
      menu.add_menu_item('1', 'SEARCH FOR EMPLOYEES BY LOCATION', SearchConst.EMPLOYEE_BY_LOCATION)
      menu.add_menu_item('2', 'SEARCH FOR BUILDINGS BY LOCATION', SearchConst.BUILDING_BY_LOCATION)
      menu.add_menu_item('3', 'SEARCH FOR EMPLOYEE BY ID', SearchConst.EMPLOYEE_BY_ID)
      menu.add_menu_item('4', 'SEARCH FOR BUILDING BY ID ', SearchConst.BUILDING_BY_ID)
      menu.add_menu_item('5', 'SEARCH FOR TASK BY ID', SearchConst.TASK_BY_ID)
      menu.add_menu_item('6', 'SEARCH FOR TASK BY BUILDINGS', SearchConst.TASK_BY_BUILDING)
      menu.add_menu_item('7', 'SEARCH FOR TASK BY EMPLOYEE', SearchConst.TASK_BY_EMPLOYEE)
      menu.add_menu_item('8', 'SEARCH FOR REPORTS BY BUILDING', SearchConst.REPORT_BY_BUILDING)
      menu.add_menu_item('9', 'SEARCH FOR REPORT BY EMPLOYEE', SearchConst.REPORT_BY_EMPLOYEE)
      options = menu.get_options()
      self.__screen.display_menu(menu)

      # Display header text using css class PAGE_HEADER
      self.__screen.print('SYSTEM SEARCH', 2, 50, 'PAGE_HEADER') # starting from line 2, col 40

      # Return options to uihandler
      return options

  def __emp_by_location_handler(self):
    ''' Handler that allows user to select a location from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    locations = self.llapi.get_all_locations()
    table = Table(locations, LocConst.TABLE_HEADERS)
    question_text = 'ENTER NUMBER (#) OF LOCATION'
    location = self.__screen.select_from_table(table, 3, question_text)
    self.llapi.set_param(EmpConst.INPUT_PARAM, location)
    return EmpConst.FILTER_LOCATION

  def __build_by_location_handler(self):
    ''' Handler that allows user to select a location from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    locations = self.llapi.get_all_locations()
    table = Table(locations, LocConst.TABLE_HEADERS)
    question_text = 'ENTER NUMBER (#) OF LOCATION'
    location = self.__screen.select_from_table(table, 3, question_text)
    self.llapi.set_param(BuildConst.INPUT_PARAM, location)
    return BuildConst.FILTER_LOCATION

  def __emp_by_id_handler(self):
    pass

  def __build_by_id_handler(self):
    pass

  def __task_by_id_handler(self):
    pass

  def __task_by_building_handler(self):
    ''' Handler that allows user to select a location from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    buildings = self.llapi.get_all_buildings()
    table = Table(buildings, BuildConst.TABLE_HEADERS)
    question_text = 'ENTER NUMBER (#) OF BUILDING'
    building = self.__screen.select_from_table(table, 3, question_text)
    self.llapi.set_param(TaskConst.INPUT_PARAM, building)
    return TaskConst.FILTER_BUILDING

  def __task_by_emp_handler(self):
    ''' Handler that allows user to select a location from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    employees = self.llapi.get_all_employees()
    table = Table(employees, EmpConst.TABLE_HEADERS)
    question_text = 'ENTER NUMBER (#) OF EMPLOYEE'
    employee = self.__screen.select_from_table(table, 3, question_text)
    self.llapi.set_param(TaskConst.INPUT_PARAM, employee)
    return TaskConst.FILTER_EMPLOYEE

  def __report_by_build_handler(self):
    ''' Handler that allows user to select a location from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    buildings = self.llapi.get_all_buildings()
    table = Table(buildings, BuildConst.TABLE_HEADERS)
    question_text = 'ENTER NUMBER (#) OF BUILDING'
    building = self.__screen.select_from_table(table, 3, question_text)
    self.llapi.set_param(ReportConst.INPUT_PARAM, building)
    return ReportConst.FILTER_BUILDING

  def __report_by_emp_handler(self):
    ''' Handler that allows user to select a location from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    employees = self.llapi.get_all_employees()
    table = Table(employees, EmpConst.TABLE_HEADERS)
    question_text = 'ENTER NUMBER (#) OF EMPLOYEE'
    employee = self.__screen.select_from_table(table, 3, question_text)
    self.llapi.set_param(ReportConst.INPUT_PARAM, employee)
    return ReportConst.FILTER_EMPLOYEE

