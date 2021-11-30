from llapi import LlApi
from ui.screen import Screen
from ui.viewframe import ViewFrame
from ui.building import BuildingView
from ui.location import LocationView
from ui.employee import EmployeeView
from ui.contractor import ContractorView
from ui.task import TaskView
from ui.report import ReportView
from ui.login import LoginView
from ui.mainmenu import MainMenuView
from ui.search import SearchView

class UiHandler():

  def __init__(self):
    self.__screen = Screen()
    self.__window = Screen(30, 118, 5, 1, parent=self.__screen)
    self.llapi = LlApi()
    self.__init_colors()
    self.__init_views()
    self.current_view = None
    self.breadcrumb = []
    self.current_user = None

  def __init_views(self):
    self.view_frame = ViewFrame(self.__screen)
    self.location_view = LocationView(self.__window)
    self.employee_view = EmployeeView(self.__window, self.llapi)
    self.building_view = BuildingView(self.__window)
    # self.accessory_view = AccessoryView(self.__window)
    self.task_view = TaskView(self.__window)
    self.report_view = ReportView(self.__window)
    self.contractor_view = ContractorView(self.__window)
    self.login_view = LoginView(self.__window, self.llapi)
    self.search_view = SearchView(self.__window)
    self.main_menu_view = MainMenuView(self.__window)

  def __init_colors(self):
    ''' TODO '''
    self.__screen.set_color_pair(1, 147) # Option
    self.__screen.set_color_pair(2, 160) # Error
    self.__screen.set_color_pair(3, 165) # Logo
    self.__screen.set_color_pair(4, 145) # Table header

  def quit(self):
    self.__screen.end()

  def option_style(self):
    ''' TODO '''
    return self.__screen.get_color_pair(1) + self.__screen.get_style(['BOLD'])

  def error_style(self):
    ''' TODO '''
    return self.__screen.get_color_pair(2) + self.__screen.get_style(['REVERSE'])

  def logo_style(self):
    ''' TODO '''
    return self.__screen.get_color_pair(3) + self.__screen.get_style(['BOLD'])
  
  def table_header_style(self):
    ''' TODO '''
    return self.__screen.get_color_pair(4)