from models.location import Location
from ui.form import Form
from ui.login import LoginView
from ui.table import Table
from utils import Filters
from llapi import LlApi
from ui.screen import Screen
from ui.menu import Menu
from ui.constants import LocConst, GlobalConst, Styles

class LocationView():

  def __init__(self, screen: Screen, llapi: LlApi):
    self.__screen = screen
    self.llapi = llapi
    self.__create_input_map()

  def __create_input_map(self):
    ''' Dictionary with second half of menu item connection as key and
    handler method for that selection as value. '''
    self.__input_map = {
      #'MENU': self.__menu_handler, Þurfum ekki þetta fyrir locations
      #'FILTER_LOCATION': self.__filter_location_handler, Þurfum ekki að filtera locations
      'LIST_ALL': self.__list_all_handler,
      'LIST_ALL_NEXT': self.__list_all_paging_next_handler,
      'LIST_ALL_PREV': self.__list_all_paging_prev_handler,
      'LIST_BUILDINGS': self.__list_buildings_handler,
      'LIST_EMPLOYEES': self.__list_employees_handler,
      'LIST_CONSTRACTORS': self.__list_contractors_handler,
      'SELECT_FROM_LIST': self.__select_from_list_handler,
      'VIEW': self.__view_location_handler,
      'ADD_NEW': self.__new_location_handler,
      'SAVE': self.__save_location_handler,
      'EDIT': self.__edit_location_handler,
      #'GET_ID': self.__get_id_handler Þetta þarf ekki?
    } 

  ################## Handler methods #########################

  #def __menu_handler(self) Þrurfum ekki location menu!

  def __view_location_handler(self, loc: Location):
    ''' Displays information about an location. '''
    menu = Menu(13)
    menu.add_menu_item('1', 'VIEW ALL BUILDINGS', LocConst.LIST_BUILDINGS)
    menu.add_menu_item('2', 'VIEW ALL EMPLOYEES', LocConst.LIST_EMPLOYEES)
    menu.add_menu_item('3', 'VIEW ALL CONTRACTORS', LocConst.LIST_CONTRACTORS)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('/', 'EDIT', LocConst.ADMIN_EDIT)
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    
    self.__display_one_location(loc)
    self.__screen.display_menu(menu)
    # Store loc in params so edit handler can pick it up and handle editing
    self.llapi.set_param(LocConst.LOCATION_PARAM, loc)
    return options

  def __list_all_handler(self, table: Table = None):
    ''' Handler that gets a list of all Locations and displays as a table.
    If too many rows are to be displayed, paging is applied.'''
    if table is None:
      # First call to list. If table is not None, paging is being used
      loc = self.llapi.get_all_locations()
      table = self.__create_table(loc)

    # Create and display menu option that allows user to select an item from the list
    menu = Menu()
    menu.add_menu_item('V', 'SELECT LOCATION TO VIEW', LocConst.SELECT_FROM_LIST)
    self.__screen.display_menu(menu)

    # Display the table and get paging options
    paging_options = self.__screen.display_table(table)
    if 'N' in paging_options:
      menu.add_menu_item('N', 'NEXT', LocConst.LIST_ALL_NEXT)
    if 'P' in paging_options:
      menu.add_menu_item('P', 'PREVIOUS', LocConst.LIST_ALL_PREV)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', LocConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu,self.llapi.user.role))
    
    if table.pages > 0:
      # Store table so paging handlers can use paging
      self.llapi.set_param(LocConst.TABLE_PARAM, table)

    return options

  def __list_all_paging_next_handler(self):
    ''' Go to next page of location list. If table is not available
    in params, list all handler will be called and whole list from page 
    one will be displayed. '''
    try:
      # pop table from params, go to next page and call list all handler with table
      table: Table = self.llapi.get_param(LocConst.TABLE_PARAM)
      table.next_page()
      return self.__list_all_handler(table)
    except KeyError:
      return self.__list_all_handler()

  def __list_all_paging_prev_handler(self):


    ''' Go to previous page of location list. If table is not available
    in params, list all handler will be called and whole list from page 
    one will be displayed. '''
    try:
      # pop table from params, go to previous page and call list all handler with table
      table: Table = self.llapi.get_param(LocConst.TABLE_PARAM)
      table.previous_page()
      return self.__list_all_handler(table)
    except KeyError:
      return self.__list_all_handler()

  def __new_location_handler(self):
    ''' Handler to display a form to enter data for new Location. '''
    self.__screen.print('CREATE NEW LOCATION', 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE FILL THE FORM TO CREATE A NEW lOCATION', 5, 6, Styles.DATA_KEY)
    self.__screen.refresh()
    form = Form(Location.get_new_fields())
    form_window = self.__screen.display_form(form)
    for field in form:
      if field.options is not None:
        # TODO Display options list
        pass
      if field.editable:
        form_window.edit_form_field(field)
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(LocConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(18)
    menu.add_menu_item('A', 'APPLY CHANGES', LocConst.SAVE)
    menu.add_menu_item('D', 'DISCARD CHANGES', LocConst.MENU)
    self.__screen.display_menu(menu)
    return menu.get_options()

  def __save_location_handler(self):
    ''' After adding new or editing an employee, this handler will save to disk
    if user chooses to apply changes. '''
    try:
      form: Form = self.llapi.get_param(LocConst.FORM_PARAM)
    except KeyError as err:
      # This really shouldn't happen. We'll put this here anyways.
      self.__screen.print(str(err), 6, 6, Styles.ERROR)
      return {}
    try:
      # Check if form has an id field. If it does, it's an edit operation
      id = form['id']
      loc = self.llapi.update_location(form)
    except StopIteration:
      # No id present, adding new location
      loc = self.llapi.new_location(form)
    return self.__view_location_handler(loc)

  def __edit_location_handler(self):
    ''' Handler to display a form to edit Location. '''
    try:
      loc: Location = self.llapi.get_param(LocConst.LOCATION_PARAM)
    except KeyError as err:
      self.__screen.print(str(err), 6, 6, Styles.ERROR)
      return {}
    
    self.__screen.print(str(loc), 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE EDIT EACH FIELD IN THE FORM', 5, 6, Styles.DATA_KEY)
    self.__screen.refresh()

    form = Form(loc.get_edit_fields())
    form_window = self.__screen.display_form(form)
    for field in form:
      if field.options is not None:
        # TODO Display options list
        pass
      if field.editable:
        form_window.edit_form_field(field)
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(LocConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(18)
    menu.add_menu_item('A', 'APPLY CHANGES', LocConst.SAVE)
    menu.add_menu_item('D', 'DISCARD CHANGES', LocConst.LIST_ALL)
    self.__screen.display_menu(menu)
    return menu.get_options()

  def find_handler(self, input: str):
    ''' This method is called by ui handler when an Location view is requested.
    The screen is cleared before calling the requested handler and refreshed
    before returning back to ui handler to make sure everything is displayed correctly. '''
    if input not in self.__input_map:
      raise KeyError(f'Location does not have a handler for {input}')
    handler: function = self.__input_map[input]
    self.__screen.clear()
    options = handler()
    self.__screen.refresh()
    return options

  def __select_from_list_handler(self):
    ''' Handler that allows user to select an location from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    try:
      # Get table from params if available
      table: Table = self.llapi.get_param(LocConst.TABLE_PARAM)
    except KeyError:
      # Else create a new table
      locs = self.llapi.get_all_locations()
      table = self.__create_table(locs)
    
    self.__screen.print('ENTER NUMBER (#) OF LOCATION TO VIEW', 3, 6, Styles.DATA_KEY)
    while True: # Ask user to select Employee
      filter = Filters.NUMBERS
      filter += self.__screen.display_table(table)
      selection = self.__screen.get_string(3, 43, 2, filter)
      # Clear error and previous input if exists
      [self.__screen.delete_character(3, x + 43) for x in range(40)]
      try:
        # Get selected Location and send it to View handler
        row = int(selection)
        loc: LoginView = table.data[row - 1]
        self.__screen.clear() # Clears screen so view gets a clean canvas
        return self.__view_location_handler(loc)
      except IndexError:
        # User should select a correct number, display error and try again
        self.__screen.print('INVALID NUMBER', 3, 60, Styles.ERROR)
      except ValueError:
        # Switching pages
        key = selection.upper()
        if key == 'P':
          table.previous_page()
        elif key == 'N':
          table.next_page()
        else:
          # Fat fingers, should only press either P or N and then Enter
          self.__screen.flash()

  def __list_buildings_handler(self):
    pass

  def __list_employees_handler(self):
    pass
  
  def __list_contractors_handler(self):
    pass

  def __create_table(self, locs: 'list[Location]', begin_line: int = 5) -> Table:
    ''' Create a Table object from a list of Locations. Table class takes in
    a list of employee instances and list of headers to create a table. '''
    headers = {
      'id': 'ID',
      'airport': 'AIRPORT',
      'country': 'COUNTRY',
      'city': 'CITY',
      'manager': 'MANAGER',
      'phone': 'PHONE MUMBER'
    }
    return Table(locs, headers, begin_line)

  def __display_one_location(self, loc: Location) -> None:
    ''' Displays information about an location on the screen. '''
    left_column = Menu(7,6,15)
    left_column.add_menu_item('AIRPORT', loc.airport)
    left_column.add_menu_item('OPENING HOURS', loc.opening_hours)
    left_column.add_menu_item('ADDRESS', loc.address)
    self.__screen.display_menu(left_column, Styles.DATA_KEY)

    middle_column = Menu(7, 46, 10)
    middle_column.add_menu_item('MANAGER', loc.manager)
    middle_column.add_menu_item('PHONE', str(loc.phone))
    self.__screen.display_menu(middle_column, Styles.DATA_KEY)

    right_column = Menu(7, 86, 20)
    right_column.add_menu_item('TOTAL BUILDINGS', str(len(loc.buildings)))
    right_column.add_menu_item('TOTAL EMPLOYEES', str(len(loc.employees)))
    right_column.add_menu_item('TOTAL CONTRACTORS', str(len(loc.contractors)))
    self.__screen.display_menu(right_column, Styles.DATA_KEY)

    self.__screen.print('-----------------------------------------------------------------------------------------------------------',11,6)
    self.__screen.print('-----------------------------------------------------------------------------------------------------------',5,6)
    header_text = '#{}  {}, {}'.format(str(loc.id),loc.city,loc.country)
    self.__screen.print(header_text,3,59-(len(header_text) // 2))

  def find_handler(self, input: str):
    ''' This method is called by ui handler when an Location view is requested.
    The screen is cleared before calling the requested handler and refreshed
    before returning back to ui handler to make sure everything is displayed correctly. '''
    if input not in self.__input_map:
      raise KeyError(f'Location does not have a handler for {input}')
    handler: function = self.__input_map[input]
    self.__screen.clear()
    options = handler()
    self.__screen.refresh()
    return options