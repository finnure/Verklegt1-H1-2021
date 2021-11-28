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
    self.__screen = Screen(main=True)
    self.__window = Screen(30, 118, 5, 1)
    self.llapi = LlApi()
    self.__init_views()
    # ask for login
    # display main view
    pass

  def __init_views(self):
    self.view_frame = ViewFrame(self.__screen)
    self.location_view = LocationView(self.__window)
    self.employee_view = EmployeeView(self.__window)
    self.building_view = BuildingView(self.__window)
    # self.accessory_view = AccessoryView(self.__window)
    self.task_view = TaskView(self.__window)
    self.report_view = ReportView(self.__window)
    self.contractor_view = ContractorView(self.__window)
    self.login_view = LoginView(self.__window)
    self.search_view = SearchView(self.__window)
    self.main_menu_view = MainMenuView(self.__window)
