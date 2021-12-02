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
    self.__init_views()
    self.__init_menu()
    self.current_view = None
    self.breadcrumb = []
    self.current_user = None

  def __init_views(self):
    self.login_view = LoginView(self.__window, self.llapi)
    self.view_frame = ViewFrame(self.__screen)
    self.main_menu_view = MainMenuView(self.__window)
    self.location_view = LocationView(self.__window)
    self.employee_view = EmployeeView(self.__window, self.llapi)
    self.building_view = BuildingView(self.__window)
    # self.accessory_view = AccessoryView(self.__window)
    self.task_view = TaskView(self.__window)
    self.report_view = ReportView(self.__window)
    self.contractor_view = ContractorView(self.__window)
    self.search_view = SearchView(self.__window)

    self.view_map: 'LocationView | EmployeeView | BuildingView | TaskView | ReportView | ContractorView | SearchView | MainMenuView' = {
      'LOCATION': self.location_view,
      'EMPLOYEE': self.employee_view,
      'BUILDING': self.building_view,
      'TASK': self.task_view,
      'REPORT': self.report_view,
      'CONTRACTOR': self.contractor_view,
      'SEARCH': self.search_view,
      'MENU': self.main_menu_view,
    }

  def __init_colors(self):
    ''' TODO '''
    self.__screen.set_color_pair(1, 147) # Option
    self.__screen.set_color_pair(2, 160) # Error
    self.__screen.set_color_pair(3, 165) # Logo
    self.__screen.set_color_pair(4, 145) # Table header

  def __init_menu(self):
    header_menu = Menu()
    header_menu.add_menu_item('L', '(L)ocations', 'LOCATION:MENU')
    header_menu.add_menu_item('B', '(B)uilding', 'BUILDING:MENU')
    header_menu.add_menu_item('E', '(E)mployee', 'EMPLOYEE:MENU')
    header_menu.add_menu_item('T', '(T)asks', 'TASK:MENU')
    header_menu.add_menu_item('C', '(C)ontractors', 'CONTRACTOR:MENU')
    header_menu.add_menu_item('S', '(S)earch', 'SEARCH:MENU')
    global_options = header_menu.get_options()
    self.header_menu = header_menu

    footer_menu = Menu()
    footer_menu.add_menu_item('H', '(H)ome', 'MENU:MENU')
    footer_menu.add_menu_item('-', '(-)Back', 'SELF:BACK')
    footer_menu.add_menu_item('O', 'Log (O)ut', 'SELF:LOGOUT')
    footer_menu.add_menu_item('Q', '(Q)uit', 'SELF:QUIT')
    global_options.update(footer_menu.get_options())
    self.footer_menu = footer_menu
    self.global_options = global_options




  def start(self):
    ''' All the magic starts here! '''
    user = self.login_view.get_input()
    if user is None:
      return
    else:
      self.view_frame.print_view()
      self.llapi.set_logged_in_user(user)
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