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
from ui.menu import Menu

class UiHandler():

  def __init__(self):
    self.__screen = Screen()
    self.__window = Screen(30, 118, 5, 1, parent=self.__screen)
    self.llapi = LlApi()
    self.__init_colors()
    self.__init_menu()
    self.__init_views()
    self.current_view = None
    self.breadcrumb = []
    self.current_user = None

  def __init_views(self):
    self.login_view = LoginView(self.__window, self.llapi)
    self.view_frame = ViewFrame(self.__screen, self.llapi, self.header_menu, self.footer_menu)
    self.main_menu_view = MainMenuView(self.__window)
    self.location_view = LocationView(self.__window)
    self.employee_view = EmployeeView(self.__window, self.llapi)
    self.building_view = BuildingView(self.__window)
    # self.accessory_view = AccessoryView(self.__window)
    self.task_view = TaskView(self.__window)
    self.report_view = ReportView(self.__window)
    self.contractor_view = ContractorView(self.__window)
    self.search_view = SearchView(self.__window)

    self.view_map = {
      'LOCATION': self.location_view,
      'EMPLOYEE': self.employee_view,
      'BUILDING': self.building_view,
      'TASK': self.task_view,
      'REPORT': self.report_view,
      'CONTRACTOR': self.contractor_view,
      'SEARCH': self.search_view,
      'MENU': self.main_menu_view,
      'SELF': self
    }

  def __init_colors(self):
    ''' Setup color pairs for css classes. Available classes are:
    ERROR, FRAME_TEXT, OPTION, LOGO_NAME, LOGO_TEXT, TABLE_HEADER, PAGE_HEADER, DATA_KEY '''
    self.__screen.set_color_pair(1, 160, 254) # ERROR Rautt/Hvítt
    self.__screen.set_color_pair(2, 75) # FRAME_TEXT Blátt
    self.__screen.set_color_pair(3, 123) # OPTION Gult
    self.__screen.set_color_pair(4, 165) # LOGO_NAME Bleikt
    self.__screen.set_color_pair(5, 147) # LOGO_TEXT Cyan
    self.__screen.set_color_pair(6, 75) # TABLE_HEADER 
    self.__screen.set_color_pair(7, 75) # PAGE_HEADER
    self.__screen.set_color_pair(8, 75) # DATA_KEY

  def __init_menu(self):
    header_menu = Menu()
    header_menu.add_menu_item('L', '(L)OCATIONS', 'LOCATION:MENU')
    header_menu.add_menu_item('B', '(B)UILDING', 'BUILDING:MENU')
    header_menu.add_menu_item('E', '(E)MPLOYEE', 'EMPLOYEE:MENU')
    header_menu.add_menu_item('T', '(T)ASKS', 'TASK:MENU')
    header_menu.add_menu_item('C', '(C)ONTRACTORS', 'CONTRACTOR:MENU')
    header_menu.add_menu_item('S', '(S)EARCH', 'SEARCH:MENU')
    global_options = header_menu.get_options()
    self.header_menu = header_menu

    footer_menu = Menu()
    footer_menu.add_menu_item('H', '(H)OME', 'MENU:MENU')
    footer_menu.add_menu_item('-', '(-) BACK', 'SELF:BACK')
    footer_menu.add_menu_item('Z', '(Z) LOG OUT', 'SELF:LOGOUT')
    footer_menu.add_menu_item('Q', '(Q)UIT', 'SELF:QUIT')
    global_options.update(footer_menu.get_options())
    self.footer_menu = footer_menu
    self.global_options = global_options

  def start(self):
    ''' All the magic starts here! '''
    user = self.login_view.get_input()
    if user is None:
      return
    else:
      self.llapi.set_logged_in_user(user)
      self.view_frame.print_view()
      options: dict = self.employee_view.find_handler('MENU')
      while True:
        self.__screen.flush_input()
        selection = self.__screen.get_character()
        key = selection.upper()
        if key in self.global_options:
          self.breadcrumb = []
          self.current_view = self.global_options[key]
        elif key in options:
          self.breadcrumb.append(self.current_view)
          self.current_view = options[key]
        else:
          # Invalid option selected, flash and try again
          self.__screen.flash()
          continue
        view_key, handler_key = self.current_view.split(':')
        if view_key not in self.view_map:
          raise KeyError(f'View not available for {view_key}')
        view = self.view_map[view_key]
        options = view.find_handler(handler_key)

  def find_handler(self, input: str):
    pass
        
  def quit(self):
    self.__screen.end()
