from llapi import LlApi
from models.contractor import Contractor
from models.employee import Employee
from models.task import Task
from ui.screen import Screen
from models.report import ContractorReport, EmployeeReport, Report
from ui.form import Form
from ui.table import Table
from ui.menu import Menu
from utils import Filters
from ui.constants import AccConst, ContrConst, ReportConst, GlobalConst, LocConst, ReportConst, Styles, TaskConst

class ReportView():

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
      'VIEW': self.__view_handler,
      'ADD_NEW': self.__add_new_handler,
      'NEW_CONTRACTOR': self.__add_contractor_report_handler,
      'SAVE': self.__save_handler,
      'GET_ID': self.__get_id_handler,
      'FILTER_TASK': self.__filter_task_handler,
      'FILTER_EMPLOYEE': self.__filter_employee_handler,
      'FILTER_CONTRACTOR': self.__filter_contractor_handler,
      'FILTER_BUILDING': self.__filter_building_handler,
    }

  def find_handler(self, input: str):
    ''' This method is called by ui handler when an Report view is requested.
    The screen is cleared before calling the requested handler and refreshed
    before returning back to ui handler to make sure everything is displayed correctly. '''
    if input not in self.__input_map:
      raise KeyError(f'Report does not have a handler for {input}')
    handler: function = self.__input_map[input]
    self.__screen.clear()
    options = handler()
    self.__screen.refresh()
    return options


  def __filter_task_handler(self):
    ''' Handler that gets a list of all Reports and displays as a table.
    If too many rows are to be displayed, paging is applied.'''
    # Get task from params
    try:
      task: Task = self.llapi.get_param(ReportConst.INPUT_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, 'ERROR')
      return {}
    reports = self.llapi.get_reports_for_task(task.id)
    table = Table(reports, ReportConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return ReportConst.LIST_ALL

  def __filter_employee_handler(self):
    ''' Handler that gets a list of all Reports and displays as a table.
    If too many rows are to be displayed, paging is applied.'''
    # Get task from params
    try:
      employee: Employee = self.llapi.get_param(ReportConst.INPUT_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, 'ERROR')
      return {}
    reports = self.llapi.get_reports_for_employee(employee.id)
    table = Table(reports, ReportConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return ReportConst.LIST_ALL

  def __filter_contractor_handler(self):
    ''' Handler that gets a list of all Reports and displays as a table.
    If too many rows are to be displayed, paging is applied.'''
    # Get task from params
    try:
      contractor: Contractor = self.llapi.get_param(ReportConst.INPUT_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, 'ERROR')
      return {}
    reports = self.llapi.get_reports_for_contractor(contractor.id)
    table = Table(reports, ReportConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return ReportConst.LIST_ALL

  def __filter_building_handler(self):
    ''' Handler that gets a list of all Reports and displays as a table.
    If too many rows are to be displayed, paging is applied.'''
    # Get task from params
    try:
      building: Task = self.llapi.get_param(ReportConst.INPUT_PARAM)
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, 'ERROR')
      return {}
    reports = self.llapi.get_reports_for_building(building.id)
    table = Table(reports, ReportConst.TABLE_HEADERS)
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)
    return ReportConst.LIST_ALL

  def __list_all_handler(self):
    ''' Handler that gets a list of all Reports and displays as a table.
    If too many rows are to be displayed, paging is applied.'''
    try:
      table: Table = self.llapi.get_param(GlobalConst.TABLE_PARAM)
      if not isinstance(table.data[0], Report):
        raise KeyError
    except (KeyError, IndexError):
      # First call to list. If table is not None, paging is being used
      reports = self.llapi.get_all_reports()
      table = Table(reports, ReportConst.TABLE_HEADERS)

    # Create and display menu option that allows user to select an item from the list
    menu = Menu()
    menu.add_menu_item('V', 'SELECT A REPORT TO VIEW', ReportConst.SELECT_FROM_LIST)
    self.__screen.display_menu(menu)

    # Display the table and get paging options
    paging_options = self.__screen.display_table(table)
    if 'N' in paging_options:
      menu.add_menu_item('N', 'NEXT', GlobalConst.PAGING_NEXT)
    if 'P' in paging_options:
      menu.add_menu_item('P', 'PREVIOUS', GlobalConst.PAGING_PREV)
    options = menu.get_options()

    admin_menu = Menu(2, 13, 10)
    admin_menu.add_menu_item('+', 'ADD NEW', ReportConst.ADMIN_NEW)
    options.update(self.__screen.display_admin_menu(admin_menu,self.llapi.user.role))
    
    # Store table so paging handlers can use paging
    self.llapi.set_param(GlobalConst.TABLE_PARAM, table)

    return options

  def __select_from_list_handler(self):
    ''' Handler that allows user to select an Report from a list.
    Available input is either a row number or an available paging option.
    If wrong row number is selected, an error is displayed and user asked
    to try again. '''
    try:
      # Get table from params if available
      table: Table = self.llapi.get_param(GlobalConst.TABLE_PARAM)
    except KeyError:
      # Else create a new table
      reports = self.llapi.get_all_reports()
      table = Table(reports, ReportConst.TABLE_HEADERS)
    
    question_text = 'ENTER NUMBER (#) OF REPORT TO VIEW'
    report = self.__screen.select_from_table(table, 3, question_text)
    self.llapi.set_param(ReportConst.REPORT_PARAM, report)
    return ReportConst.VIEW

  def __get_id_handler(self):
    ''' Ask user to enter id of report to find. '''
    options = self.__menu_handler()
    self.__screen.print('PLEASE ENTER ID:', 8, 10)
    report_id = self.__screen.get_string(8, 28, 3, Filters.NUMBERS, editing=True)
    report = self.llapi.get_report(int(report_id))
    if report is None:
      self.__screen.print(f'NO REPORT FOUND WITH ID {report_id}', 10, 10, Styles.ERROR)
      self.__screen.print('PRESS I TO SEARCH AGAIN', 11, 10)
      self.__screen.paint_character('OPTION', 11, 16)
      return options
    # Report found, clear screen and call view handler to display info
    self.llapi.set_param(ReportConst.REPORT_PARAM, report)
    return ReportConst.VIEW

  def __view_handler(self):
    ''' Displays information about a report. '''
    try:
      report: Report = self.llapi.get_param(ReportConst.REPORT_PARAM)
    except KeyError:
      self.__screen.print('NO REPORT FOUND TO DISPLAY', 6, 6, 'ERROR')
      return {}

    menu = Menu(14)
    menu.add_menu_item('2', 'VIEW LOCATION INFORMATION', LocConst.VIEW)

    admin_menu = Menu(2, 20)
    admin_menu.add_menu_item('V', 'APPROVE REPORT', ReportConst.ADMIN_APPROVE)
    admin_menu.add_menu_item('G', 'RATE CONTRACTOR', ContrConst.RATE)
    
    self.__display_one_report(report)
    #self.__screen.display_menu(menu)

    options = menu.get_options()
    options.update(self.__screen.display_admin_menu(admin_menu, self.llapi.user.role))

    # Store report in params so other handlers can pick it up to display relative data
    self.llapi.set_param(ReportConst.REPORT_PARAM, report)
    return options

  def __display_one_report(self, report: EmployeeReport) -> None:
    ''' Displays information about an employee on the screen. '''

    # display header info
    text = str(report)
    self.__screen.print(text, 2, 59 - (len(text) // 2), 'PAGE_HEADER')
    self.__screen.horizontal_line(50, 3, 34)

    c_reps = report.contractor_reports
    if len(c_reps) == 1:
      contractor = c_reps[0].contractor.name
    else:
      contractor = str(len(c_reps))
    con_fee = sum([rep.contractor_fee for rep in c_reps])
    total_cost = con_fee + report.material_cost + report.labor_cost

    left_column = Menu(5, spacing=14)
    left_column.add_menu_item('BUILDING', report.building.registration)
    left_column.add_menu_item('ADDRESS', report.building.address)
    left_column.add_menu_item('REPORT DATE', report.report_date)
    left_column.add_menu_item('TASK TYPE', report.task.type)
    left_column.add_menu_item('EMPLOYEE', report.employee.name)
    left_column.add_menu_item('CONTRACTOR', contractor)
    self.__screen.display_menu(left_column, Styles.DATA_KEY)

    right_column = Menu(5, 60, 18)
    right_column.add_menu_item('MATERIAL COST', f'{report.material_cost} {GlobalConst.CURRENCY}')
    right_column.add_menu_item('LABOUR COST', f'{report.labor_cost} {GlobalConst.CURRENCY}')
    right_column.add_menu_item('CONTRACTOR FEE', f'{con_fee} {GlobalConst.CURRENCY}')
    right_column.add_menu_item('TOTAL COST', f'{total_cost} {GlobalConst.CURRENCY}')
    right_column.add_menu_item('TASK STATUS', report.task.status)
    right_column.add_menu_item('REPORT APPROVED', report.approved.upper())
    self.__screen.display_menu(right_column, Styles.DATA_KEY)

    self.__screen.horizontal_line(100, 12, 6)

    self.__screen.print('TASK DESCRIPTION', 14, 6, Styles.DATA_KEY)
    self.__screen.print(report.task.title, 15, 6)

    self.__screen.print('REPORT DESCRIPTION', 17, 6, Styles.DATA_KEY)
    self.__screen.print(report.description, 18, 6)

    self.__screen.print('NOTE', 20, 6, Styles.DATA_KEY)
    self.__screen.print(report.note, 21, 6)


  def __add_new_handler(self):
    ''' Handler to display a form to enter data for new Report. '''
    try:
      task = self.llapi.get_param(ReportConst.INPUT_PARAM)
      if not isinstance(task, Task):
        raise KeyError('NO TASK FOUND TO REPORT ON')
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    self.__screen.print('CREATE NEW REPORT', 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE FILL THE FORM TO CREATE A NEW REPORT', 5, 6, Styles.DATA_KEY)
    self.__screen.refresh()
    form = Form(EmployeeReport.get_new_fields())
    for field in form:
      if field.key == 'task_id':
        field.value = task.id
      if field.key == 'employee_id':
        field.value = self.llapi.user.id
    form_window = self.__screen.display_form(form)
    for field in form:
      if field.options is not None:
        # TODO Display options list
        pass
      if field.editable:
        form_window.edit_form_field(field)
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(ReportConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(18)
    menu.add_menu_item('A', 'APPLY CHANGES', ReportConst.SAVE)
    menu.add_menu_item('D', 'DISCARD CHANGES', ReportConst.MENU)
    self.__screen.display_menu(menu)
    return menu.get_options()

  def __add_contractor_report_handler(self):
    ''' Handler to display a form to enter data for new Report. '''
    try:
      report = self.llapi.get_param(ReportConst.INPUT_PARAM)
      if not isinstance(report, EmployeeReport):
        raise KeyError('NO REPORT FOUND TO ADD CONTRACTOR TO')
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    try:
      contractor = self.llapi.get_param(ContrConst.CONTRACTOR_PARAM)
      if not isinstance(contractor, Contractor):
        raise KeyError('NO CONTRACTOR FOUND TO REPORT ON')
    except KeyError as err:
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    self.__screen.print('CREATE NEW REPORT', 2, 50, Styles.PAGE_HEADER)
    self.__screen.print('PLEASE FILL THE FORM TO CREATE A NEW REPORT', 5, 6, Styles.DATA_KEY)
    self.__screen.refresh()
    form = Form(ContractorReport.get_new_fields())
    for field in form:
      if field.key == 'employee_report_id':
        field.value = report.id
      if field.key == 'contractor_id':
        field.value = contractor.id
    form_window = self.__screen.display_form(form)
    for field in form:
      if field.options is not None:
        # TODO Display options list
        pass
      if field.editable:
        form_window.edit_form_field(field)
    
    # Save form in params so the save handler can pick it up and save data to disk
    self.llapi.set_param(ReportConst.FORM_PARAM, form)

    # Delete outdated message and display menu options
    self.__screen.delete_character(5, 6, 50)
    menu = Menu(18)
    menu.add_menu_item('A', 'APPLY CHANGES', ReportConst.SAVE)
    menu.add_menu_item('D', 'DISCARD CHANGES', ReportConst.MENU)
    self.__screen.display_menu(menu)
    return menu.get_options()

  def __save_handler(self):
    ''' After adding new or editing an report, this handler will save to disk
    if user chooses to apply changes. '''
    try:
      form: Form = self.llapi.get_param(ReportConst.FORM_PARAM)
    except KeyError as err:
      # This really shouldn't happen. We'll put this here anyways.
      self.__screen.print(str(err).upper(), 6, 6, Styles.ERROR)
      return {}
    try:
      # Check if form has a task_id field. If it does, it's an EmployeeReport
      _ = form['task_id']
      report = self.llapi.new_employee_report(form)
    except StopIteration:
      # No task_id present, it's a ContractorReport
      contractor_report = self.llapi.new_contractor_report(form)
      report = self.llapi.get_report(contractor_report.employee_report_id)
    self.llapi.set_param(ReportConst.REPORT_PARAM, report)
    return ReportConst.VIEW

