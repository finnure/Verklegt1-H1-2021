from llapi import LlApi
from models.accessory import Accessory
from models.location import Location
from ui.screen import Screen
from models.building import Building
from ui.form import Form
from ui.table import Table
from ui.menu import Menu
from utils import Filters
from ui.constants import AccConst, BuildConst, GlobalConst, LocConst, ReportConst, Styles, TaskConst


class BuildingView():

  def __init__(self, screen):
    self.__screen = screen

  def __init__(self, screen: Screen, llapi: LlApi):
    self.__screen = screen
    self.llapi = llapi
    self.__create_input_map()

  def __create_input_map(self):
    ''' Dictionary with second half of menu item connection as key and
    handler method for that selection as value. '''
    self.__input_map = {
      'MENU': self.__menu_handler,
      'LIST_ALL': self.__list_all_handler,
      'SELECT_FROM_LIST': self.__select_from_list_handler,
      'VIEW': self.__view_handler,
      'ADD_NEW': self.__add_new_handler,
      'SAVE': self.__save_handler,
      'EDIT': self.__edit_handler,
      'GET_ID': self.__get_id_handler,
      'FILTER_LOCATION': self.__filter_location_handler,
    }

  def find_handler(self, input: str):
    ''' This method is called by ui handler when an Building view is requested.
    The screen is cleared before calling the requested handler and refreshed
    before returning back to ui handler to make sure everything is displayed correctly. '''
    if input not in self.__input_map:
      raise KeyError(f'Building does not have a handler for {input}')
    handler: function = self.__input_map[input]
    self.__screen.clear()
    options = handler()
    self.__screen.refresh()
    return options

    ################## Handler methods #########################

  def __menu_handler(self):
    ''' Displays Building main menu and returns options and connections as a list'''
    text = 'BUILDING MENU'
    self.__screen.print(text, 2, 59 - (len(text) // 2), 'PAGE_HEADER')
    self.__screen.horizontal_line(50, 3, 34)
    menu = Menu(5, 6)
    menu.add_menu_item('I', 'SEARCH FOR BUILDING BY ID', BuildConst.GET_ID)
    menu.add_menu_item('A', 'VIEW ALL BUILDINGS', BuildConst.LIST_ALL)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', BuildConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    self.__screen.display_menu(menu)
    return options

      ################## List handlers #####################

  def __list_all_handler(self):
    ''' Handler that gets a list of all Buildings and displays as a table.
    If too many rows are to be displayed, paging is applied.'''
    try:
      table: Table = self.llapi.get_param(GlobalConst.TABLE_PARAM)
      if not isinstance(table.data[0], Building):
        raise KeyError
    except (KeyError, IndexError):
      # First call to list. If table is not None, paging is being used
      buildings = self.llapi.get_all_buildings()
      table = Table(buildings, BuildConst.TABLE_HEADERS)

    # Create and display menu option that allows user to select an item from the list
    menu = Menu()
    menu.add_menu_item('V', 'SELECT A BUILDING TO VIEW', BuildConst.SELECT_FROM_LIST)
    self.__screen.display_menu(menu)

    # Display the table and get paging options
    paging_options = self.__screen.display_table(table)
    if 'N' in paging_options:
      menu.add_menu_item('N', 'NEXT', GlobalConst.PAGING_NEXT)
    if 'P' in paging_options:
      menu.add_menu_item('P', 'PREVIOUS', GlobalConst.PAGING_PREV)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', BuildConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu,self.llapi.user.role))
    
    # Store table so paging handlers can use paging
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)

    return options

  def __select_from_list_handler(self):
    ''' Handler that allows user to select an Building from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    try:
      # Get table from params if available
      table: Table = self.llapi.get_param(GlobalConst.TABLE_PARAM)
    except KeyError:
      # Else create a new table
      buildings = self.llapi.get_all_buildings()
      table = Table(buildings, BuildConst.TABLE_HEADERS)
    
    question_text = 'ENTER NUMBER (#) OF BUILDING TO VIEW'
    building = self.__screen.select_from_table(table, 3, question_text)
    self.llapi.set_param(BuildConst.BUILDING_PARAM, building)
    return BuildConst.VIEW

  def __get_id_handler(self):
    ''' Ask user to enter id of building to find. '''
    options = self.__menu_handler()
    self.__screen.print('PLEASE ENTER ID:', 11, 10)
    building_id = self.__screen.get_string(11, 28, 3, Filters.NUMBERS, editing=True)
    building = self.llapi.get_building(int(building_id))
    if building is None:
      self.__screen.print(f'NO BUILDING FOUND WITH ID {building_id}', 13, 10, Styles.ERROR)
      self.__screen.print('PRESS I TO SEARCH AGAIN', 14, 10)
      self.__screen.paint_character('OPTION', 14, 16)
      return options
    # Building found, clear screen and call view handler to display info
    self.llapi.set_param(BuildConst.BUILDING_PARAM, building)
    return BuildConst.VIEW

  def __view_handler(self):
    ''' Displays information about a building. '''
    try:
      building: Building = self.llapi.get_param(BuildConst.BUILDING_PARAM)
    except KeyError:
      self.__screen.print('NO BUILDING FOUND TO DISPLAY', 6, 6, 'ERROR')
      return {}

    try:
      table: Table = self.llapi.get_param(GlobalConst.TABLE_PARAM)
      if not isinstance(table.data[0], Accessory):
        raise KeyError
    except (KeyError, IndexError):
      # If table is not available or is not an Accessory table, create new table
      accessories = self.llapi.get_accessories_for_building(building.id)
      table = Table(accessories, AccConst.TABLE_HEADERS, 14, 6, 8, False)

    menu = Menu(14)
    menu.add_menu_item('1', 'VIEW ACTIVE TASKS', TaskConst.FILTER_BUILDING)
    menu.add_menu_item('2', 'VIEW LOCATION INFORMATION', LocConst.VIEW)
    menu.add_menu_item('3', 'VIEW REPORTS', ReportConst.FILTER_BUILDING)

    admin_menu = Menu(2, 18)
    admin_menu.add_menu_item('/', 'EDIT BUILDING', BuildConst.ADMIN_EDIT)
    admin_menu.add_menu_item('+', 'ADD BUILDING', BuildConst.ADMIN_NEW)
    admin_menu.add_menu_item('W', 'ADD TASK', TaskConst.ADMIN_NEW)
    admin_menu.add_menu_item('Y', 'ADD ACCESSORY', AccConst.ADMIN_NEW)
    
    self.__display_one_building(building)
    self.__screen.display_menu(menu)

    if building.accessory_count > 0:
      # Only display accessories if they exist
      self.__screen.print('ACCESSORIES', 12, 6, Styles.DATA_KEY)
      paging_options = self.__screen.display_table(table)
      if 'N' in paging_options:
        menu.add_menu_item('N', 'NEXT', GlobalConst.PAGING_NEXT)
      if 'P' in paging_options:
        menu.add_menu_item('P', 'PREVIOUS', GlobalConst.PAGING_PREV)
      self.llapi.set_param(GlobalConst.TABLE_PARAM, table)

    options = menu.get_options()
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))

    # Store location so location view gets something to view
    location = self.llapi.get_location(building.location_id)
    self.llapi.set_param(LocConst.LOCATION_PARAM, location)
    # Store building in params so other handlers can pick it up to display relative data
    self.llapi.set_param(BuildConst.BUILDING_PARAM, building)
    self.llapi.set_param(TaskConst.INPUT_PARAM, building)
    self.llapi.set_param(AccConst.INPUT_PARAM, building)
    return options

  def __display_one_building(self, building: Building) -> None:
    ''' Displays information about an employee on the screen. '''

    # display header info
    text = str(building)
    self.__screen.print(text, 2, 59 - (len(text) // 2), 'PAGE_HEADER')
    self.__screen.horizontal_line(50, 3, 34)

    left_column = Menu(5, spacing=14)
    left_column.add_menu_item('TYPE', building.type)
    left_column.add_menu_item('ROOMS', building.rooms)
    left_column.add_menu_item('STATE', building.state)
    left_column.add_menu_item('DESCRIPTION', building.description)
    self.__screen.display_menu(left_column, Styles.DATA_KEY)

    right_column = Menu(5, 46, 20)
    right_column.add_menu_item('ACTIVE TASKS', str(building.task_count))
    right_column.add_menu_item('UNAPPROVED REPORTS', str(building.size))
    right_column.add_menu_item('ACCESSORIES', str(building.accessory_count))
    right_column.add_menu_item('SIZE IN M2', str(building.size))
    self.__screen.display_menu(right_column, Styles.DATA_KEY)

    self.__screen.horizontal_line(100, 10, 6)


  def __add_new_handler(self):
    ''' Handler to display a form to enter data for new Building. '''
    self.__screen.print('CREATE NEW BUILDING', 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE FILL THE FORM TO CREATE A NEW BUILDING', 5, 6, Styles.DATA_KEY)
    self.__screen.refresh()
    form = Form(Building.get_new_fields())
    form_window = self.__screen.display_form(form)
    for field in form:
      if field.options is not None:
        # TODO Display options list
        pass
      if field.editable:
        form_window.edit_form_field(field)
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(BuildConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(18)
    menu.add_menu_item('A', 'APPLY CHANGES', BuildConst.SAVE)
    menu.add_menu_item('D', 'DISCARD CHANGES', BuildConst.MENU)
    self.__screen.display_menu(menu)
    return menu.get_options()

  def __edit_handler(self):
    ''' Handler to display a form to edit Building. '''
    try:
      building: Building = self.llapi.get_param(BuildConst.BUILDING_PARAM)
    except KeyError as err:
      self.__screen.print(str(err), 6, 6, Styles.ERROR)
      return {}
    
    self.__screen.print(str(building), 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE EDIT EACH FIELD IN THE FORM', 5, 6, Styles.DATA_KEY)
    self.__screen.refresh()

    form = Form(building.get_edit_fields())
    form_window = self.__screen.display_form(form)
    for field in form:
      if field.options is not None:
        # TODO Display options list
        pass
      if field.editable:
        form_window.edit_form_field(field)
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(BuildConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(18)
    menu.add_menu_item('A', 'APPLY CHANGES', BuildConst.SAVE)
    menu.add_menu_item('D', 'DISCARD CHANGES', BuildConst.MENU)
    self.__screen.display_menu(menu)
    return menu.get_options()

  def __save_handler(self):
    ''' After adding new or editing an building, this handler will save to disk
    if user chooses to apply changes. '''
    try:
      form: Form = self.llapi.get_param(BuildConst.FORM_PARAM)
    except KeyError as err:
      # This really shouldn't happen. We'll put this here anyways.
      self.__screen.print(str(err), 6, 6, Styles.ERROR)
      return {}
    try:
      # Check if form has an id field. If it does, it's an edit operation
      _ = form['id']
      building = self.llapi.update_building(form)
    except StopIteration:
      # No id present, adding new building
      building = self.llapi.new_building(form)
    self.llapi.set_param(BuildConst.BUILDING_PARAM, building)
    return BuildConst.VIEW

  def __filter_location_handler(self):
    try:
      location: Location = self.llapi.get_param(BuildConst.INPUT_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    buildings = self.llapi.get_buildings_by_location(location.id)
    table = Table(buildings, BuildConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return BuildConst.LIST_ALL
