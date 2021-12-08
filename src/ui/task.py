from llapi import LlApi
from models.building import Building
from models.employee import Employee
from ui.screen import Screen
from models.task import Task
from ui.form import Form
from ui.table import Table
from ui.menu import Menu
from utils import Filters, Helpers
from ui.constants import AccConst, BuildConst, EmpConst, GlobalConst, ReportConst, TaskConst, LocConst, Styles, TaskConst


class TaskView():

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
      'FILTER_EMPLOYEE': self.__filter_employee_handler,
      'FILTER_BUILDING': self.__filter_building_handler,
    }

  def find_handler(self, input: str):
    ''' This method is called by ui handler when an Task view is requested.
    The screen is cleared before calling the requested handler and refreshed
    before returning back to ui handler to make sure everything is displayed correctly. '''
    if input not in self.__input_map:
      raise KeyError(f'Task does not have a handler for {input}')
    handler: function = self.__input_map[input]
    self.__screen.clear()
    options = handler()
    self.__screen.refresh()
    return options

    ################## Handler methods #########################

  def __menu_handler(self):
    ''' Displays Task main menu and returns options and connections as a list'''
    menu = Menu(2, 6)
    menu.add_menu_item('I', 'SEARCH FOR TASK BY ID', TaskConst.GET_ID)
    menu.add_menu_item('A', 'VIEW ALL TASKS', TaskConst.LIST_ALL)
    menu.add_menu_item('F', 'VIEW TASKS BY LOCATION', TaskConst.FILTER_LOCATION)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', TaskConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    self.__screen.display_menu(menu)
    return options

      ################## List handlers #####################

  def __list_all_handler(self, table: Table = None):
    ''' Handler that gets a list of all Tasks and displays as a table.
    If too many rows are to be displayed, paging is applied.'''
    try:
      table: Table = self.llapi.get_param(GlobalConst.TABLE_PARAM)
      if not isinstance(table.data[0], Task):
        raise KeyError
    except (KeyError, IndexError):
      # First call to list. If table is not None, paging is being used
      tasks = self.llapi.get_all_tasks()
      table = Table(tasks, TaskConst.TABLE_HEADERS)

    # Create and display menu option that allows user to select an item from the list
    menu = Menu()
    menu.add_menu_item('V', 'SELECT A TASK TO VIEW', TaskConst.SELECT_FROM_LIST)
    self.__screen.display_menu(menu)

    # Display the table and get paging options
    paging_options = self.__screen.display_table(table)
    if 'N' in paging_options:
      menu.add_menu_item('N', 'NEXT', GlobalConst.PAGING_NEXT)
    if 'P' in paging_options:
      menu.add_menu_item('P', 'PREVIOUS', GlobalConst.PAGING_PREV)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', TaskConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu,self.llapi.user.role))
    
    # Store table so paging handlers can use paging
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)

    return options

  def __select_from_list_handler(self):
    ''' Handler that allows user to select an Task from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    try:
      # Get table from params if available
      table: Table = self.llapi.get_param(TaskConst.TABLE_PARAM)
    except KeyError:
      # Else create a new table
      tasks = self.llapi.get_all_tasks()
      table = Table(tasks, TaskConst.TABLE_HEADERS)

    question_text = 'ENTER NUMBER (#) OF TASK TO VIEW'
    task = self.__screen.select_from_table(table, 3, question_text)
    self.llapi.set_param(TaskConst.TASK_PARAM, task)
    return TaskConst.VIEW


  def __get_id_handler(self):
    ''' Ask user to enter id of task to find. '''
    options = self.__menu_handler()
    self.__screen.print('PLEASE ENTER ID:', 8, 10)
    task_id = self.__screen.get_string(8, 28, 3, Filters.NUMBERS)
    task = self.llapi.get_task(int(task_id))
    if task is None:
      self.__screen.print(f'NO TASK FOUND WITH ID {task_id}', 10, 10, Styles.ERROR)
      self.__screen.print('PRESS I TO SEARCH AGAIN', 11, 10)
      self.__screen.paint_character('OPTION', 11, 16)
      return options
    # Task found, clear screen and call view handler to display info
    self.llapi.set_param(TaskConst.TASK_PARAM, task)
    return TaskConst.VIEW

  def __view_handler(self):
    ''' Displays information about a task. '''
    try:
      task: Task = self.llapi.get_param(TaskConst.TASK_PARAM)
    except KeyError:
      self.__screen.print('NO TASK FOUND TO DISPLAY', 3, 6, 'ERROR')
      return {}
    menu = Menu(18)
    menu.add_menu_item('1', 'VIEW REPORTS', ReportConst.FILTER_TASK)
    menu.add_menu_item('2', 'VIEW BUILDING INFORMATION', BuildConst.VIEW)
    options = menu.get_options()

    admin_menu = Menu(2, 18)
    admin_menu.add_menu_item('/', 'EDIT TASK', TaskConst.ADMIN_EDIT)
    admin_menu.add_menu_item('+', 'ADD TASK', TaskConst.ADMIN_NEW)
    admin_menu.add_menu_item('W', 'ADD TASK', TaskConst.ADMIN_NEW)
    admin_menu.add_menu_item('Y', 'ADD ACCESSORY', AccConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))
    
    self.__display_one_task(task)
    self.__screen.display_menu(menu)
    # Store task in params so edit handler can pick it up and handle editing
    self.llapi.set_param(ReportConst.INPUT_PARAM, task)
    self.llapi.set_param(TaskConst.TASK_PARAM, task)
    building = self.llapi.get_building(task.building_id)
    self.llapi.set_param(BuildConst.BUILDING_PARAM, building)
    return options

  def __display_one_task(self, task: Task) -> None:
    ''' Displays information about an employee on the screen. '''

    # display header info
    text = str(task)
    self.__screen.print(text, 2, 59 - (len(text) // 2), 'PAGE_HEADER')
    self.__screen.horizontal_line(50, 3, 34)

    left_column = Menu(5, spacing=10)
    left_column.add_menu_item('TYPE', task.type)
    left_column.add_menu_item('STATE', task.priority)
    left_column.add_menu_item('LOCATION', str(task.building_id))
    self.__screen.display_menu(left_column, Styles.DATA_KEY)

    right_column = Menu(5, 46, 14)
    right_column.add_menu_item('ROOMS', task.recurring)
    right_column.add_menu_item('SIZE', task.status)
    right_column.add_menu_item('ACTIVE TASKS', '10')
    self.__screen.display_menu(right_column, Styles.DATA_KEY)

    self.__screen.print('DESCRIPTION', 10, 6, Styles.DATA_KEY)
    lines = Helpers.get_multiline_string(task.short_description, 50)
    for line, text in enumerate(lines):
      self.__screen.print(text, 10 + line, 20)
    self.__screen.horizontal_line(100, 16, 6)

  def __add_new_handler(self):
    ''' Handler to display a form to enter data for new Task. '''
    self.__screen.print('CREATE NEW TASK', 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE FILL THE FORM TO CREATE A NEW TASK', 5, 6, Styles.DATA_KEY)
    self.__screen.refresh()
    form = Form(Task.get_new_fields())
    form_window = self.__screen.display_form(form)
    for field in form:
      if field.options is not None:
        # TODO Display options list
        pass
      if field.editable:
        form_window.edit_form_field(field)
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(TaskConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(18)
    menu.add_menu_item('A', 'APPLY CHANGES', TaskConst.SAVE)
    menu.add_menu_item('D', 'DISCARD CHANGES', TaskConst.MENU)
    self.__screen.display_menu(menu)
    return menu.get_options()

  def __edit_handler(self):
    ''' Handler to display a form to edit Task. '''
    try:
      task: Task = self.llapi.get_param(TaskConst.TASK_PARAM)
    except KeyError as err:
      self.__screen.print(str(err), 6, 6, Styles.ERROR)
      return {}
    
    self.__screen.print(str(task), 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE EDIT EACH FIELD IN THE FORM', 5, 6, Styles.DATA_KEY)
    self.__screen.refresh()

    form = Form(task.get_edit_fields())
    form_window = self.__screen.display_form(form)
    for field in form:
      if field.options is not None:
        # TODO Display options list
        pass
      if field.editable:
        form_window.edit_form_field(field)
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(TaskConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(18)
    menu.add_menu_item('A', 'APPLY CHANGES', TaskConst.SAVE)
    menu.add_menu_item('D', 'DISCARD CHANGES', TaskConst.MENU)
    self.__screen.display_menu(menu)
    return menu.get_options()

  def __save_handler(self):
    ''' After adding new or editing an task, this handler will save to disk
    if user chooses to apply changes. '''
    try:
      form: Form = self.llapi.get_param(TaskConst.FORM_PARAM)
    except KeyError as err:
      # This really shouldn't happen. We'll put this here anyways.
      self.__screen.print(str(err), 6, 6, Styles.ERROR)
      return {}
    try:
      # Check if form has an id field. If it does, it's an edit operation
      _ = form['id']
      task = self.llapi.update_task(form)
    except StopIteration:
      # No id present, adding new task
      task = self.llapi.new_task(form)
    self.llapi.set_param(TaskConst.TASK_PARAM, task)
    return TaskConst.VIEW

  def __filter_location_handler(self):
    options = self.__menu_handler()
    return options

  def __filter_employee_handler(self):
    try:
      emp: Employee = self.llapi.get_param(TaskConst.INPUT_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    tasks = self.llapi.get_active_tasks_for_user(emp.id)
    table = Table(tasks, TaskConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return TaskConst.LIST_ALL

  def __filter_building_handler(self):
    try:
      building: Building = self.llapi.get_param(TaskConst.INPUT_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    tasks = self.llapi.get_active_tasks_for_user(building.id)
    table = Table(tasks, TaskConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return TaskConst.LIST_ALL
