from models.location import Location
from ui.form import Form
from ui.login import LoginView
from ui.table import Table
from utils import Filters
from llapi import LlApi
from ui.screen import Screen
from ui.menu import Menu
from ui.constants import LocConst,EmpConst, ContrConst, BuildConst, GlobalConst, Styles

class LocationView():

  def __init__(self, screen: Screen, llapi: LlApi):
    self.__screen = screen
    self.llapi = llapi
    self.__create_input_map()

  def __create_input_map(self):
    ''' Dictionary with second half of menu item connection as key and
    handler method for that selection as value. '''
    self.__input_map = {
      'LIST_ALL': self.__list_all_handler,
      'SELECT_FROM_LIST': self.__select_from_list_handler,
      'VIEW': self.__view_location_handler,
      'ADD_NEW': self.__new_location_handler,
      'SAVE': self.__save_location_handler,
      'EDIT': self.__edit_location_handler,
    } 

  ################## Handler methods #########################

  def __view_location_handler(self):
    ''' Displays information about an location. '''
    try:
      loc = self.llapi.get_param(LocConst.LOCATION_PARAM)
    except KeyError:
      self.__screen.print('NO LOCATION FOUND TO DISPLAY', 6, 6, Styles.ERROR)
      return {}
    menu = Menu(16)
    menu.add_menu_item('1', 'VIEW ALL BUILDINGS', BuildConst.FILTER_LOCATION)
    menu.add_menu_item('2', 'VIEW ALL EMPLOYEES', EmpConst.FILTER_LOCATION)
    menu.add_menu_item('3', 'VIEW ALL CONTRACTORS', ContrConst.FILTER_LOCATION)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('/', 'EDIT', LocConst.ADMIN_EDIT)
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    
    self.__display_one_location(loc)
    self.__screen.display_menu(menu)

    # Store location in Building, Employee and Contractor params for them to pick it up
    self.llapi.set_param(BuildConst.INPUT_PARAM, loc)
    self.llapi.set_param(EmpConst.INPUT_PARAM, loc)
    self.llapi.set_param(ContrConst.INPUT_PARAM, loc)
    # Store loc in params so edit handler can pick it up and handle editing
    self.llapi.set_param(LocConst.LOCATION_PARAM, loc)
    return options

  def __list_all_handler(self):
    ''' Handler that gets a list of all Locations and displays as a table.
    If too many rows are to be displayed, paging is applied.'''
    try:
      table: Table = self.llapi.get_param(GlobalConst.TABLE_PARAM)
      if not isinstance(table.data[0], Location):
        raise KeyError
    except (KeyError, IndexError):
      # First call to list. If table is not None, paging is being used
      loc = self.llapi.get_all_locations()
      table = Table(loc, LocConst.TABLE_HEADERS)

    text = 'LOCATION LIST'
    self.__screen.print(text, 2, 59 - (len(text) // 2), 'PAGE_HEADER')
    self.__screen.horizontal_line(50, 3, 34)
    # Create and display menu option that allows user to select an item from the list
    menu = Menu(5)
    menu.add_menu_item('V', 'SELECT LOCATION TO VIEW', LocConst.SELECT_FROM_LIST)
    self.__screen.display_menu(menu)

    # Display the table and get paging options
    paging_options = self.__screen.display_table(table)
    if 'N' in paging_options:
      menu.add_menu_item('N', 'NEXT', GlobalConst.PAGING_NEXT)
    if 'P' in paging_options:
      menu.add_menu_item('P', 'PREVIOUS', GlobalConst.PAGING_PREV)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', LocConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu,self.llapi.user.role))
    
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)

    return options


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
    menu.add_menu_item('D', 'DISCARD CHANGES', LocConst.LIST_ALL)
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
      table = Table(locs, LocConst.TABLE_HEADERS)
    
    text = 'LOCATION LIST'
    self.__screen.print(text, 2, 59 - (len(text) // 2), 'PAGE_HEADER')
    self.__screen.horizontal_line(50, 3, 34)
    question_text = 'ENTER NUMBER (#) OF LOCATION TO VIEW'
    location = self.__screen.select_from_table(table, 5, question_text)
    self.llapi.set_param(LocConst.LOCATION_PARAM, location)
    return LocConst.VIEW

  def __display_one_location(self, loc: Location) -> None:
    ''' Displays information about an location on the screen. '''
    left_column = Menu(7,6,15)
    left_column.add_menu_item('AIRPORT', loc.airport)
    left_column.add_menu_item('OPENING HOURS', loc.opening_hours)
    left_column.add_menu_item('PHONE', loc.phone)
    left_column.add_menu_item('ADDRESS', loc.address)
    self.__screen.display_menu(left_column, Styles.DATA_KEY)

    right_column = Menu(7, 50, 20)
    right_column.add_menu_item('TOTAL BUILDINGS', str(len(loc.buildings)))
    right_column.add_menu_item('TOTAL EMPLOYEES', str(len(loc.employees)))
    right_column.add_menu_item('TOTAL CONTRACTORS', str(len(loc.contractors)))
    self.__screen.display_menu(right_column, Styles.DATA_KEY)

    self.__screen.horizontal_line(100, 5, 6)
    self.__screen.horizontal_line(100, 13, 6)
    header_text = str(loc)
    self.__screen.print(header_text, 3, 59 - (len(header_text) // 2))

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