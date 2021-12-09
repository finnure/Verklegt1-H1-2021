from llapi import LlApi
from models.building import Building
from models.contractor import Contractor
from models.employee import Employee
from models.location import Location
from ui.screen import Screen
from models.task import Task
from ui.form import Form, FormField
from ui.table import Table
from ui.menu import Menu
from utils import Filters, Helpers, Validate
from ui.constants import AccConst, BuildConst, EmpConst, GlobalConst, ReportConst, Roles, TaskConst, LocConst, Styles, TaskConst


class TaskView():

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
      'ASSIGN': self.__assign_handler,
      'COMPLETE': self.__complete_handler,
      'APPROVE': self.__approve_handler,
      'SAVE': self.__save_handler,
      'EDIT': self.__edit_handler,
      'GET_ID': self.__get_id_handler,
      'FILTER_MY_ACTIVE': self.__filter_my_active_handler,
      'FILTER_LOCATION': self.__filter_location_handler,
      'FILTER_EMPLOYEE': self.__filter_employee_handler,
      'FILTER_BUILDING': self.__filter_building_handler,
      'FILTER_CONTRACTOR': self.__filter_contractor_handler,
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
    menu.add_menu_item('M', 'VIEW MY ACTIVE TASKS', TaskConst.FILTER_MY_ACTIVE)
    menu.add_menu_item('1', 'VIEW TASKS BY BUILDING', TaskConst.FILTER_BUILDING, Roles.MANAGER)
    menu.add_menu_item('2', 'VIEW TASKS BY EMPLOYEE', TaskConst.FILTER_EMPLOYEE, Roles.MANAGER)
    menu.add_menu_item('3', 'VIEW TASKS BY LOCATION', TaskConst.FILTER_LOCATION, Roles.MANAGER)
    menu.add_menu_item('4', 'VIEW TASKS BY CONTRACTOR', TaskConst.FILTER_CONTRACTOR, Roles.MANAGER)
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
      table: Table = self.llapi.get_param(GlobalConst.TABLE_PARAM)
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
    menu = Menu(22)
    menu.add_menu_item('1', 'ASSIGN TO ME', TaskConst.ASSIGN)
    menu.add_menu_item('2', 'COMPLETE', TaskConst.COMPLETE)
    menu.add_menu_item('3', 'VIEW REPORTS', ReportConst.FILTER_TASK)
    menu.add_menu_item('4', 'ADD REPORT', ReportConst.ADMIN_NEW)
    menu.add_menu_item('5', 'VIEW BUILDING', BuildConst.VIEW)
    options = menu.get_options()

    admin_menu = Menu(2, 18)
    admin_menu.add_menu_item('/', 'EDIT TASK', TaskConst.ADMIN_EDIT)
    admin_menu.add_menu_item('+', 'ADD TASK', TaskConst.ADMIN_NEW)
    admin_menu.add_menu_item('A', 'APPROVE', TaskConst.ADMIN_APPROVE)

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

    self.__screen.print('TITLE', 5, 6, Styles.DATA_KEY)
    self.__screen.print(task.title, 5, 22)
    self.__screen.print('DESCRIPTION', 7, 6, Styles.DATA_KEY)
    lines = Helpers.get_multiline_string(task.short_description, 50)
    for line, text in enumerate(lines):
      self.__screen.print(text, 7 + line, 22)

    left_column = Menu(12, spacing=16)
    left_column.add_menu_item('START DATE', task.start_date)
    left_column.add_menu_item('END DATE', task.due_date)
    left_column.add_menu_item('LAST MODIFIED', task.modified)
    left_column.add_menu_item('TASK TYPE', task.type)
    left_column.add_menu_item('RECURRENT', task.recurring.upper())
    if task.recurring.lower().startswith('y'):
      try:
        repeats = TaskConst.REPEATS[task.repeats_every]
      except KeyError:
        repeats = task.repeats_every
      left_column.add_menu_item('REPEATS EVERY', repeats)
    self.__screen.display_menu(left_column, Styles.DATA_KEY)

    right_column = Menu(12, 46, 14)
    right_column.add_menu_item('BUILDING', task.recurring.upper())
    right_column.add_menu_item('EST COST', f'{task.estimated_cost} ISK')
    right_column.add_menu_item('EMPLOYEE', task.employee_name if task.employee_id is not None else None)
    right_column.add_menu_item('STATUS', task.status)
    right_column.add_menu_item('TOTAL COST', f'{self.llapi.calculate_task_cost(task)} ISK')
    self.__screen.display_menu(right_column, Styles.DATA_KEY)

    self.__screen.horizontal_line(100, 20, 6)

  def __assign_handler(self):
    ''' Assign task to logged in employee. '''
    try:
      task: Task = self.llapi.get_param(TaskConst.TASK_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    task.employee_id = self.llapi.user.id
    task.status = 'Assigned'
    updated_task = self.llapi.update_task_property(task)
    self.llapi.set_param(TaskConst.TASK_PARAM, updated_task)
    return GlobalConst.BACK

  def __complete_handler(self):
    ''' Assign task to logged in employee. '''
    try:
      task: Task = self.llapi.get_param(TaskConst.TASK_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    task.employee_id = self.llapi.user.id
    task.status = 'Completed'
    updated_task = self.llapi.update_task_property(task)
    self.llapi.set_param(TaskConst.TASK_PARAM, updated_task)
    return GlobalConst.BACK

  def __approve_handler(self):
    ''' Assign task to logged in employee. '''
    try:
      task: Task = self.llapi.get_param(TaskConst.TASK_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    task.status = 'Approved'
    updated_task = self.llapi.update_task_property(task)
    self.llapi.set_param(TaskConst.TASK_PARAM, updated_task)
    return GlobalConst.BACK

  def __add_new_handler(self):
    ''' Handler to display a form to enter data for new Task. '''
    try:
      building: Building = self.llapi.get_param(TaskConst.INPUT_PARAM)
    except KeyError:
      self.__screen.print('NO BUILDING SELECTED TO ADD TASK TO. PLEASE SELECT A BUILDING FIRST', 6, 6, Styles.ERROR)
      return {}
    self.__screen.print('CREATE NEW TASK', 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE FILL THE FORM TO CREATE A NEW TASK', 5, 6, Styles.DATA_KEY)
    self.__screen.print('DATE FORMAT', 7, 6, Styles.DATA_KEY)
    self.__screen.print('YYYY-MM-DD', 7, 19)
    self.__screen.refresh()
    form = Form(Task.get_new_fields())
    for field in form:
      if field.key == 'building_id':
        field.value = building.id
      if field.key == 'location_id':
        field.value = building.location_id
    form_window = self.__screen.display_form(form, 9)
    for field in form:
      options_window = None
      if field.options is not None:
        options_window: Screen = form_window.display_form_menu(field.options)
      if field.editable:
        form_window.edit_form_field(field)
      if options_window:
        options_window.clear()
        options_window.refresh()
        form_window.refresh()
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(TaskConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(23, 6)
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
    self.__screen.print('DATE FORMAT', 7, 6, Styles.DATA_KEY)
    self.__screen.print('YYYY-MM-DD', 7, 19)
    self.__screen.refresh()

    form = Form(task.get_edit_fields())
    form_window = self.__screen.display_form(form, 9)
    for field in form:
      options_window = None
      if field.options is not None:
        options_window: Screen = form_window.display_form_menu(field.options)
      if field.editable:
        form_window.edit_form_field(field)
      if options_window:
        options_window.clear()
        options_window.refresh()
        form_window.refresh()
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(TaskConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(24)
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

  def __filter_my_active_handler(self):
    tasks = self.llapi.get_tasks_for_employee(self.llapi.user.id, ['assigned'])
    table = Table(tasks, TaskConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return TaskConst.LIST_ALL

  def __filter_location_handler(self):
    try:
      loc: Location = self.llapi.get_param(TaskConst.INPUT_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    statuses, from_date, to_date = self.__get_filter_for_task()
    tasks = self.llapi.get_tasks_for_location(loc.id, statuses, from_date, to_date)
    table = Table(tasks, TaskConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return TaskConst.LIST_ALL

  def __filter_employee_handler(self):
    try:
      emp: Employee = self.llapi.get_param(TaskConst.INPUT_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    statuses, from_date, to_date = self.__get_filter_for_task()
    tasks = self.llapi.get_tasks_for_employee(emp.id, statuses, from_date, to_date)
    table = Table(tasks, TaskConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return TaskConst.LIST_ALL

  def __filter_building_handler(self):
    try:
      building: Building = self.llapi.get_param(TaskConst.INPUT_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    statuses, from_date, to_date = self.__get_filter_for_task()
    tasks = self.llapi.get_tasks_for_building(building.id, statuses, from_date, to_date)
    table = Table(tasks, TaskConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return TaskConst.LIST_ALL

  def __filter_contractor_handler(self):
    try:
      contractor: Contractor = self.llapi.get_param(TaskConst.INPUT_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    statuses, from_date, to_date = self.__get_filter_for_task()
    tasks = self.llapi.get_tasks_for_contractor(contractor.id, statuses, from_date, to_date)
    table = Table(tasks, TaskConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return TaskConst.LIST_ALL

  def __get_filter_for_task(self):
    available = True
    assigned = self.llapi.user.role == Roles.MANAGER
    completed = self.llapi.user.role == Roles.MANAGER
    approved = False
    menu = Menu(7, 6, 5)
    menu.add_menu_item('1', 'AVAILABLE')
    menu.add_menu_item('2', 'ASSIGNED')
    menu.add_menu_item('3', 'COMPLETED')
    menu.add_menu_item('4', 'APPROVED')
    menu.add_menu_item('5', 'SELECT DATE RANGE')

    from_date = FormField('from_date', 'FROM DATE', None, 1, 10, Filters.DATE, validators=[Validate.date])
    to_date = FormField('to_date', 'TO DATE', None, 1, 10, Filters.DATE, validators=[Validate.date])
    form = Form([from_date, to_date])
    while True:
      self.__screen.clear()
      self.__screen.print('SELECT FILTERS. END SELECTION WITH ', 3, 6, Styles.DATA_KEY)
      self.__screen.print('0', style=Styles.OPTION)
      self.__screen.print('INCLUDED STATUSES', 5, 6, Styles.DATA_KEY)
      self.__screen.display_menu(menu)
      self.__screen.print_selected(available, 7, 9)
      self.__screen.print_selected(assigned, 8, 9)
      self.__screen.print_selected(completed, 9, 9)
      self.__screen.print_selected(approved, 10, 9)
      self.__screen.refresh()
      while True:
        from_date = form['from_date']
        to_date = form['to_date']
        if from_date is not None and from_date != '':
          self.__screen.print('DATE FORMAT = YYYY-MM-DD', 13, 6)
          self.__screen.print('IF TO DATE IS OMITTED, ONLY REPORTS ON SELECTED FROM DATE WILL BE DISPLAYED', 14, 6)
          self.__screen.print('FROM DATE', 16, 6, Styles.DATA_KEY)
          self.__screen.print(from_date, 16, 17)
        else:
          to_date = None
        if to_date is not None and to_date != '':
          self.__screen.print('TO DATE', 17, 6, Styles.DATA_KEY)
          self.__screen.print(to_date, 17, 17)
        selection = self.__screen.get_character()
        if selection in '012345':
          break
        else:
          self.__screen.flash()
      if selection == '5':
        window = self.__screen.display_form(form, 16)
        self.__screen.print('DATE FORMAT = YYYY-MM-DD', 13, 6)
        self.__screen.print('IF TO DATE IS OMITTED, ONLY REPORTS ON SELECTED FROM DATE WILL BE DISPLAYED', 14, 6)
        self.__screen.refresh()
        for field in form:
          window.edit_form_field(field)
      elif selection == '1':
        available = not available
      elif selection == '2':
        assigned = not assigned
      elif selection == '3':
        completed = not completed
      elif selection == '4':
        approved = not approved
      elif selection == '0':
        statuses = []
        if available:
          statuses.append('available')
        if assigned:
          statuses.append('assigned')
        if completed:
          statuses.append('completed')
        if approved:
          statuses.append('approved')
        from_date = form['from_date']
        to_date = form['to_date']
        from_date = None if from_date == '' else from_date
        to_date = None if to_date == '' else to_date
        return (statuses, from_date, to_date)
