from typing import Callable
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
    self.current_view: str = None
    self.breadcrumb: 'list[str]' = []
    self.current_user = None

  def __init_views(self):
    self.login_view = LoginView(self.__window, self.llapi)
    self.view_frame = ViewFrame(self.__screen, self.llapi, self.header_menu, self.footer_menu)
    self.main_menu_view = MainMenuView(self.__window)
    self.location_view = LocationView(self.__window, self.llapi)
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
      'GLOBAL': self
    }

  def __init_colors(self):
    ''' Setup color pairs for css classes. Available classes are:
    ERROR, FRAME_TEXT, OPTION, LOGO_NAME, LOGO_TEXT, TABLE_HEADER, PAGE_HEADER, DATA_KEY, DISABLED, EDITING '''
    self.__screen.set_color_pair(1, 160, 254) # ERROR Rautt/Hvítt
    self.__screen.set_color_pair(2, 75) # FRAME_TEXT Blátt
    self.__screen.set_color_pair(3, 123) # OPTION Gult
    self.__screen.set_color_pair(4, 165) # LOGO_NAME Bleikt
    self.__screen.set_color_pair(5, 147) # LOGO_TEXT Cyan
    self.__screen.set_color_pair(6, 75) # TABLE_HEADER 
    self.__screen.set_color_pair(7, 75) # PAGE_HEADER
    self.__screen.set_color_pair(8, 75) # DATA_KEY
    self.__screen.set_color_pair(9, 8) # DISABLED
    self.__screen.set_color_pair(10, 254, 236) # EDITING

  def __init_menu(self):
    header_menu = Menu()
    header_menu.add_menu_item('L', '(L)OCATIONS', 'LOCATION:LIST_ALL')
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
      self.current_view = 'EMPLOYEE:MENU' # Debugging
      options: dict = self.employee_view.find_handler('MENU') # Debugging, replace with main menu
      while True:
        # Get input from user
        self.__screen.flush_input()
        selection = self.__screen.get_character()
        key = selection.upper()

        # Check if selection is in global options
        if key in self.global_options:
          connection = self.global_options[key]
          view_key, handler_key = connection.split(':')
          if view_key == 'SELF':
            if handler_key == 'QUIT':
              # Returning False from start will quit
              return False
            elif handler_key == 'LOGOUT':
              # Clear screen and logged in user and return True to run start() again
              self.__screen.clear()
              self.__screen.refresh()
              self.llapi.clear_logged_in_user()
              self.breadcrumb = []
              return True
            elif handler_key == 'BACK':
              if len(self.breadcrumb) <= 0:
                # Nothing to go back to, flash and continue
                self.__screen.flash()
                continue
              else:
                # set current view to last view in breadcrumb
                self.current_view = self.breadcrumb.pop()
                # next execution should use current view to find handler
            else:
              raise ValueError(f'Invalid handler key for self: {handler_key}')
          else:
            # Global menu option selected. Set it as current view and clear breadcrumbs
            self.breadcrumb = []
            self.current_view = connection
            # next execution should use current view to find handler

        # selection is not in globacl options, check current view options
        elif key in options:
          if self.current_view is not None: # Don't add None to breadcrumbs
            self.breadcrumb.append(self.current_view)
          self.current_view = options[key]

        # Invalid option selected, flash and try again
        else:
          self.__screen.flash()
          continue

        # Find and call handler for selected view
        view_key, handler_key = self.current_view.split(':')
        if view_key not in self.view_map:
          raise KeyError(f'View not available for {view_key}')
        view = self.view_map[view_key]
        options = view.find_handler(handler_key)
        
  def find_handler(self, handler_key):
    ''' Generic handler for global options if view_key is GLOBAL. '''
    if handler_key == 'BACK':
      if len(self.breadcrumb) <= 0:
        # Nothing to go back to, flash and continue
        self.__screen.flash()
        return ''
      else:
        # set current view to last view in breadcrumb
        self.current_view = self.breadcrumb.pop()
        view_key, handler_key = self.current_view.split(':')
        if view_key not in self.view_map:
          raise KeyError(f'View not available for {view_key}')
        view = self.view_map[view_key]
        return view.find_handler(handler_key)



  def quit(self):
    self.__screen.end()
