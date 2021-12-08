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
from ui.table import Table
from ui.constants import BuildConst, ContrConst, EmpConst, LocConst, SearchConst, TaskConst, GlobalConst

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
    self.location_view = LocationView(self.__window, self.llapi)
    self.main_menu_view = MainMenuView(self.__window, self.llapi, self.header_menu)
    self.employee_view = EmployeeView(self.__window, self.llapi)
    self.building_view = BuildingView(self.__window, self.llapi)
    # self.accessory_view = AccessoryView(self.__window)
    self.task_view = TaskView(self.__window, self.llapi)
    self.report_view = ReportView(self.__window, self.llapi)
    self.contractor_view = ContractorView(self.__window, self.llapi)
    self.search_view = SearchView(self.__window, self.llapi)

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
    header_menu = Menu(9)
    header_menu.add_menu_item('L', '(L)OCATIONS', LocConst.LIST_ALL)
    header_menu.add_menu_item('B', '(B)UILDINGS', BuildConst.MENU)
    header_menu.add_menu_item('E', '(E)MPLOYEES', EmpConst.MENU)
    header_menu.add_menu_item('T', '(T)ASKS', TaskConst.MENU)
    header_menu.add_menu_item('C', '(C)ONTRACTORS', ContrConst.MENU)
    header_menu.add_menu_item('S', '(S)EARCH', SearchConst.MENU)
    global_options = header_menu.get_options()
    self.header_menu = header_menu

    footer_menu = Menu()
    footer_menu.add_menu_item('H', '(H)OME', GlobalConst.MAIN_MENU)
    footer_menu.add_menu_item('-', '(-) BACK', GlobalConst.BACK)
    footer_menu.add_menu_item('Z', '(Z) LOG OUT', GlobalConst.LOGOUT)
    footer_menu.add_menu_item('Q', '(Q)UIT', GlobalConst.QUIT)
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
      self.current_view = 'MENU:MENU'
      options: dict = self.main_menu_view.find_handler('MENU')
      while True:
        # Get input from user
        self.__screen.flush_input()
        selection = self.__screen.get_character()
        try:
          key = selection.upper()
        except AttributeError:
          key = selection

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
              else:
                # pop last view from breadcrumb and display it
                options = self.find_connection(self.breadcrumb.pop())
            else:
              raise ValueError(f'Invalid handler key for self: {handler_key}')
          else:
            # Global menu option selected. Set it as current view and set home as breadcrumb
            self.breadcrumb = ['MENU:MENU']
            options = self.find_connection(connection)

        # selection is not in global options, check current view options
        elif key in options:
          if self.current_view is not None: # Don't add None to breadcrumbs
            self.breadcrumb.append(self.current_view)
          options = self.find_connection(options[key])

        # Invalid option selected, flash and try again
        else:
          self.__screen.flash()

  def find_handler(self, handler_key: str):
    ''' Generic handler for global options if view_key is GLOBAL. '''
    if handler_key == 'BACK':
      if len(self.breadcrumb) <= 0:
        # Nothing to go back to, flash and continue
        self.__screen.flash()
        return ''
      else:
        return self.find_connection(self.breadcrumb.pop())
    elif handler_key.startswith('PAGING'):
      table: Table = self.llapi.get_param(GlobalConst.TABLE_PARAM)
      if handler_key == 'PAGING_NEXT':
        table.next_page()
      elif handler_key == 'PAGING_PREV':
        table.previous_page()
      self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
      return self.find_connection(self.breadcrumb.pop())
      

  def find_connection(self, connection: str):
    ''' Find view handler for selected option. '''
    self.current_view = connection
    # Find and call handler for selected view
    view_key, handler_key = self.current_view.split(':')
    if view_key not in self.view_map:
      raise KeyError(f'View not available for {view_key}')
    view = self.view_map[view_key]
    options = view.find_handler(handler_key)
    if type(options) is str:
      # View calling another view directly
      return self.find_connection(options)
    return options




  def quit(self):
    self.__screen.end()
