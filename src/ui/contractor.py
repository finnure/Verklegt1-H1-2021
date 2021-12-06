from ui.screen import Screen
from llapi import LlApi
from models.contractor import Contractor
from ui.form import Form
from ui.table import Table
from ui.menu import Menu
from utils import Filters
from ui.constants import AccConst, ContrConst, LocConst, ReportConst, Styles, TaskConst


class ContractorView():

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
      'LIST_ALL_NEXT': self.__list_all_paging_next_handler,
      'LIST_ALL_PREV': self.__list_all_paging_prev_handler,
      'SELECT_FROM_LIST': self.__select_from_list_handler,
      'VIEW': self.__view_handler,
      'ADD_NEW': self.__add_new_handler,
      'SAVE': self.__save_handler,
      'EDIT': self.__edit_handler,
      'GET_ID': self.__get_id_handler,
      'FILTER_LOCATION': self.__filter_location_handler,
    }

  def find_handler(self, input: str):
    ''' This method is called by ui handler when an Contractor view is requested.
    The screen is cleared before calling the requested handler and refreshed
    before returning back to ui handler to make sure everything is displayed correctly. '''
    if input not in self.__input_map:
      raise KeyError(f'Contractor does not have a handler for {input}')
    handler: function = self.__input_map[input]
    self.__screen.clear()
    options = handler()
    self.__screen.refresh()
    return options

    ################## Handler methods #########################

  def __menu_handler(self):
    ''' Displays Contractor main menu and returns options and connections as a list'''
    menu = Menu(2, 6)
    menu.add_menu_item('I', 'SEARCH FOR CONTRACTOR BY ID', ContrConst.GET_ID)
    menu.add_menu_item('A', 'VIEW ALL CONTRACTORS', ContrConst.LIST_ALL)
    menu.add_menu_item('F', 'VIEW CONTRACTORS BY LOCATION', ContrConst.FILTER_LOCATION)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', ContrConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    self.__screen.display_menu(menu)
    return options

      ################## List handlers #####################

  def __list_all_paging_next_handler(self):
    ''' Go to next page of contractor list. If table is not available
    in params, list all handler will be called and whole list from page 
    one will be displayed. '''
    try:
      # pop table from params, go to next page and call list all handler with table
      table: Table = self.llapi.get_param(ContrConst.TABLE_PARAM)
      table.next_page()
      return self.__list_all_handler(table)
    except KeyError:
      return self.__list_all_handler()

  def __list_all_paging_prev_handler(self):
    ''' Go to previous page of contractor list. If table is not available
    in params, list all handler will be called and whole list from page 
    one will be displayed. '''
    try:
      # pop table from params, go to previous page and call list all handler with table
      table: Table = self.llapi.get_param(ContrConst.TABLE_PARAM)
      table.previous_page()
      return self.__list_all_handler(table)
    except KeyError:
      return self.__list_all_handler()

  def __list_all_handler(self, table: Table = None):
    ''' Handler that gets a list of all Contractors and displays as a table.
    If too many rows are to be displayed, paging is applied.'''
    if table is None:
      # First call to list. If table is not None, paging is being used
      contractors = self.llapi.get_all_contractors()
      table = self.__create_table(contractors)

    # Create and display menu option that allows user to select an item from the list
    menu = Menu()
    menu.add_menu_item('V', 'SELECT AN CONTRACTOR TO VIEW', ContrConst.SELECT_FROM_LIST)
    self.__screen.display_menu(menu)

    # Display the table and get paging options
    paging_options = self.__screen.display_table(table)
    if 'N' in paging_options:
      menu.add_menu_item('N', 'NEXT', ContrConst.LIST_ALL_NEXT)
    if 'P' in paging_options:
      menu.add_menu_item('P', 'PREVIOUS', ContrConst.LIST_ALL_PREV)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', ContrConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu,self.llapi.user.role))
    
    if table.pages > 0:
      # Store table so paging handlers can use paging
      self.llapi.set_param(ContrConst.TABLE_PARAM, table)

    return options

  def __select_from_list_handler(self):
    ''' Handler that allows user to select an Contractor from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    try:
      # Get table from params if available
      table: Table = self.llapi.get_param(ContrConst.TABLE_PARAM)
    except KeyError:
      # Else create a new table
      contractors = self.llapi.get_all_contractors()
      if len(contractors) <= 0:
        self.__screen.print('NO CONTRACTORS FOUND', 5, 6, 'ERROR')
        return {}
      table = self.__create_table(contractors)
    
    self.__screen.print('ENTER NUMBER (#) OF CONTRACTOR TO VIEW', 3, 6, Styles.DATA_KEY)
    while True: # Ask user to select Contractor
      filter = Filters.NUMBERS
      filter += self.__screen.display_table(table)
      selection = self.__screen.get_string(3, 43, 2, filter)
      # Clear error and previous input if exists
      [self.__screen.delete_character(3, x + 43) for x in range(40)]
      try:
        # Get selected Contractor and send it to View handler
        row = int(selection)
        contractor: Contractor = table.data[row - 1]
        self.__screen.clear() # Clears screen so view gets a clean canvas
        return self.__view_handler(contractor)
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

  def __create_table(self, contractors: 'list[Contractor]', begin_line: int = 5) -> Table:
    ''' Create a Table object from a list of Contractors. Table class takes in
    a list of contractor instances and list of headers to create a table. '''
    headers = {
      'id': 'ID',
      'location_id': 'LOCATION',
      'name': 'NAME',
      'speciality': 'SPECIALITY',
      'openinghours': 'OPENING HOURS',
      'phone': 'PHONE'
    }
    return Table(contractors, headers, begin_line)

  def __get_id_handler(self):
    ''' Ask user to enter id of contractor to find. '''
    options = self.__menu_handler()
    self.__screen.print('PLEASE ENTER ID:', 8, 10)
    contractor_id = self.__screen.get_string(8, 28, 3, Filters.NUMBERS)
    contractor = self.llapi.get_contractor(int(contractor_id))
    if contractor is None:
      self.__screen.print(f'NO CONTRACTOR FOUND WITH ID {contractor_id}', 10, 10, Styles.ERROR)
      self.__screen.print('PRESS I TO SEARCH AGAIN', 11, 10)
      self.__screen.paint_character('OPTION', 11, 16)
      return options
    # Contractor found, clear screen and call view handler to display info
    self.__screen.clear()
    return self.__view_handler(contractor)

  def __view_handler(self, contractor: Contractor = None):
    ''' Displays information about a contractor. '''
    if contractor is None:
      try:
        contractor = self.llapi.get_param(ContrConst.CONTRACTOR_PARAM)
      except KeyError:
        self.__screen.print('NO CONTRACTOR FOUND TO DISPLAY', 3, 6, 'ERROR')
        return {}
    menu = Menu(14)
    menu.add_menu_item('1', 'VIEW REPORTS', ReportConst.FILTER_CONTRACTOR)
    menu.add_menu_item('2', 'VIEW LOCATION INFORMATION', LocConst.VIEW)
    options = menu.get_options()

    admin_menu = Menu(2, 18)
    admin_menu.add_menu_item('/', 'EDIT CONTRACTOR', ContrConst.ADMIN_EDIT)
    admin_menu.add_menu_item('+', 'ADD CONTRACTOR', ContrConst.ADMIN_NEW)
    admin_menu.add_menu_item('W', 'ADD TASK', TaskConst.ADMIN_NEW)
    admin_menu.add_menu_item('Y', 'ADD ACCESSORY', AccConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    
    self.__display_one_contractor(contractor)
    self.__screen.display_menu(menu)
    # Store contractor in params so edit handler can pick it up and handle editing
    self.llapi.set_param(ContrConst.CONTRACTOR_PARAM, contractor)
    return options

  def __display_one_contractor(self, contractor: Contractor) -> None:
    ''' Displays information about an employee on the screen. '''

    # display header info
    text = str(contractor)
    self.__screen.print(text, 2, 59 - (len(text) // 2), 'PAGE_HEADER')

    left_column = Menu(5, spacing=11)
    left_column.add_menu_item('NAME', contractor.name)
    left_column.add_menu_item('CONTACT', contractor.contact)
    left_column.add_menu_item('LOCATION', str(contractor.location_id))
    self.__screen.display_menu(left_column, Styles.DATA_KEY)

    right_column = Menu(5, 46, 16)
    right_column.add_menu_item('EMAIL', contractor.email)
    right_column.add_menu_item('OPENING HOURS', contractor.openinghours)
    right_column.add_menu_item('PHONE', contractor.phone)
    self.__screen.display_menu(right_column, Styles.DATA_KEY)

    self.__screen.print('SPECIALITY', 10, 6, Styles.DATA_KEY)
    self.__screen.print(contractor.speciality, 10, 20)

  def __add_new_handler(self):
    ''' Handler to display a form to enter data for new Contractor. '''
    self.__screen.print('CREATE NEW CONTRACTOR', 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE FILL THE FORM TO CREATE A NEW CONTRACTOR', 5, 6, Styles.DATA_KEY)
    self.__screen.refresh()
    form = Form(Contractor.get_new_fields())
    form_window = self.__screen.display_form(form)
    for field in form:
      if field.options is not None:
        # TODO Display options list
        pass
      if field.editable:
        form_window.edit_form_field(field)
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(ContrConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(18)
    menu.add_menu_item('A', 'APPLY CHANGES', ContrConst.SAVE)
    menu.add_menu_item('D', 'DISCARD CHANGES', ContrConst.MENU)
    self.__screen.display_menu(menu)
    return menu.get_options()

  def __edit_handler(self):
    ''' Handler to display a form to edit Contractor. '''
    try:
      contractor: Contractor = self.llapi.get_param(ContrConst.CONTRACTOR_PARAM)
    except KeyError as err:
      self.__screen.print(str(err), 6, 6, Styles.ERROR)
      return {}
    
    self.__screen.print(str(contractor), 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE EDIT EACH FIELD IN THE FORM', 5, 6, Styles.DATA_KEY)
    self.__screen.refresh()

    form = Form(contractor.get_edit_fields())
    form_window = self.__screen.display_form(form)
    for field in form:
      if field.options is not None:
        # TODO Display options list
        pass
      if field.editable:
        form_window.edit_form_field(field)
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(ContrConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(18)
    menu.add_menu_item('A', 'APPLY CHANGES', ContrConst.SAVE)
    menu.add_menu_item('D', 'DISCARD CHANGES', ContrConst.MENU)
    self.__screen.display_menu(menu)
    return menu.get_options()

  def __save_handler(self):
    ''' After adding new or editing an contractor, this handler will save to disk
    if user chooses to apply changes. '''
    try:
      form: Form = self.llapi.get_param(ContrConst.FORM_PARAM)
    except KeyError as err:
      # This really shouldn't happen. We'll put this here anyways.
      self.__screen.print(str(err), 6, 6, Styles.ERROR)
      return {}
    try:
      # Check if form has an id field. If it does, it's an edit operation
      id = form['id']
      contractor = self.llapi.update_contractor(form)
    except StopIteration:
      # No id present, adding new contractor
      contractor = self.llapi.new_contractor(form)
    return self.__view_handler(contractor)

  def __filter_location_handler(self):
    options = self.__menu_handler()
    return options
