class GlobalConst():
  ''' Global constants and connections. '''
  # Constants
  TABLE_PARAM = 'GLOBAL:TABLE'

  # Connections
  VIEW_BACK = 'GLOBAL:BACK'
  PAGING_NEXT = 'GLOBAL:PAGING_NEXT'
  PAGING_PREV = 'GLOBAL:PAGING_PREV'
  MAIN_MENU = 'MENU:MENU'
  LOGOUT = 'SELF:LOGOUT'
  QUIT = 'SELF:QUIT'
  BACK = 'SELF:BACK'

class Roles():
  MANAGER = 'MANAGER'
  EMPLOYEE = 'EMPLOYEE'
  CHUCK = 'CHUCK'

class Styles():
  ''' Constants for style names available. '''
  ERROR = 'ERROR'
  FRAME_TEXT = 'FRAME_TEXT'
  OPTION = 'OPTION'
  LOGO_NAME = 'LOGO_NAME'
  LOGO_TEXT = 'LOGO_TEXT'
  TABLE_HEADER = 'TABLE_HEADER'
  PAGE_HEADER = 'PAGE_HEADER'
  DATA_KEY = 'DATA_KEY'
  DISABLED = 'DISABLED'
  EDITING = 'EDITING'

class MenuConsts():

  # Connections
  MENU = 'MENU:MENU'

class EmpConst():
  ''' Constants and connections for EmployeeView. '''
  # Constants
  FORM_PARAM = 'EMPLOYEE:FORM'
  TABLE_PARAM = 'EMPLOYEE:TABLE'
  EMPLOYEE_PARAM = 'EMPLOYEE:EMPLOYEE'
  INPUT_PARAM = 'EMPLOYEE:INPUT'

  TABLE_HEADERS = {
    'id': 'ID',
    'name': 'NAME',
    'location_city': 'CITY',
    'mobile': 'MOBILE',
    'email': 'EMAIL'
  }

  # Connections
  ADMIN_NEW = 'EMPLOYEE:ADD_NEW'
  ADMIN_EDIT = 'EMPLOYEE:EDIT'
  MENU = 'EMPLOYEE:MENU'
  LIST_ALL = 'EMPLOYEE:LIST_ALL'
  SELECT_FROM_LIST = 'EMPLOYEE:SELECT_FROM_LIST'
  VIEW = 'EMPLOYEE:VIEW'
  SAVE = 'EMPLOYEE:SAVE'
  GET_ID = 'EMPLOYEE:GET_ID'
  FILTER_LOCATION = 'EMPLOYEE:FILTER_LOCATION'

class LocConst():
  ''' Constants and connections for LocationView. '''
  # Constants
  FORM_PARAM = 'LOCATION:FORM'
  TABLE_PARAM = 'LOCATION:TABLE'
  LOCATION_PARAM = 'LOCATION:LOCATION'
  INPUT_PARAM = 'LOCATION:INPUT'

  TABLE_HEADERS = {
    'id': 'ID',
    'airport': 'AIRPORT',
    'country': 'COUNTRY',
    'city': 'CITY',
    'phone': 'PHONE MUMBER'
  }

  # Connections
  ADMIN_NEW = 'LOCATION:ADD_NEW'
  ADMIN_EDIT = 'LOCATION:EDIT'
  FILTER_LOCATION = 'LOCATION:FILTER_LOCATION'
  LIST_ALL = 'LOCATION:LIST_ALL'
  LIST_BUILDINGS = 'LOCATION:LIST_BUILDINGS'
  LIST_EMPLOYEES = 'LOCATION:LIST_EMPLOYEES'
  LIST_CONTRACTORS = 'LOCATION:LIST_CONSTRACTORS'
  SELECT_FROM_LIST = 'LOCATION:SELECT_FROM_LIST'
  VIEW = 'LOCATION:VIEW'
  SAVE = 'LOCATION:SAVE'
  GET_ID = 'LOCATION:GET_ID'

class TaskConst():
  ''' Constants and connections for TaskView. '''
  # Constants
  FORM_PARAM = 'TASK:FORM'
  TABLE_PARAM = 'TASK:TABLE'
  TASK_PARAM = 'TASK:TASK'
  INPUT_PARAM = 'TASK:INPUT'

  TABLE_HEADERS = {
    'id': 'ID',
    'status': 'STATUS',
    'priority': 'PRIORITY',
    'start_date': 'START DATE',
    'due_date': 'DUE DATE',
    'building_reg': 'BUILDING',
    'employee_name': 'EMPLOYEE'
  }

  PRIORITIES = {
    '1': 'HIGH',
    '2': 'MEDIUM',
    '3': 'LOW',
  }

  # Connections
  ADMIN_NEW = 'TASK:ADD_NEW'
  ADMIN_EDIT = 'TASK:EDIT'
  MENU = 'TASK:MENU'
  LIST_ALL = 'TASK:LIST_ALL'
  SELECT_FROM_LIST = 'TASK:SELECT_FROM_LIST'
  VIEW = 'TASK:VIEW'
  SAVE = 'TASK:SAVE'
  GET_ID = 'TASK:GET_ID'
  FILTER_MY_ACTIVE = 'TASK:FILTER_MY_ACTIVE'
  FILTER_BUILDING = 'TASK:FILTER_BUILDING'
  FILTER_LOCATION = 'TASK:FILTER_LOCATION'
  FILTER_EMPLOYEE = 'TASK:FILTER_EMPLOYEE'
  FILTER_CONTRACTOR = 'TASK:FILTER_CONTRACTOR'



class BuildConst():
  ''' Constants and connections for BuildingView. '''
  # Constants
  FORM_PARAM = 'BUILDING:FORM'
  TABLE_PARAM = 'BUILDING:TABLE'
  BUILDING_PARAM = 'BUILDING:BUILDING'
  INPUT_PARAM = 'BUILDING:INPUT'

  TABLE_HEADERS = {
    'id': 'ID',
    'address': 'ADDRESS',
    'location_city': 'LOCATION',
    'type': 'TYPE',
    'rooms': 'ROOMS',
    'state': 'STATE',
    'task_count': 'TASKS'
  }

  # Connections
  ADMIN_NEW = 'BUILDING:ADD_NEW'
  ADMIN_EDIT = 'BUILDING:EDIT'
  MENU = 'BUILDING:MENU'
  LIST_ALL = 'BUILDING:LIST_ALL'
  LIST_ALL_NEXT = 'BUILDING:LIST_ALL_NEXT'
  LIST_ALL_PREV = 'BUILDING:LIST_ALL_PREV'
  SELECT_FROM_LIST = 'BUILDING:SELECT_FROM_LIST'
  VIEW = 'BUILDING:VIEW'
  SAVE = 'BUILDING:SAVE'
  GET_ID = 'BUILDING:GET_ID'
  FILTER_LOCATION = 'BUILDING:FILTER_LOCATION'
  

class ContrConst():
  ''' Constants and connections for ContractorView. '''
  # Constants
  FORM_PARAM = 'CONTRACTOR:FORM'
  TABLE_PARAM = 'CONTRACTOR:TABLE'
  CONTRACTOR_PARAM = 'CONTRACTOR:CONTRACTOR'
  INPUT_PARAM = 'CONTRACTOR:INPUT'

  TABLE_HEADERS = {
    'id': 'ID',
    'location_id': 'LOCATION',
    'name': 'NAME',
    'speciality': 'SPECIALITY',
    'openinghours': 'OPENING HOURS',
    'phone': 'PHONE'
  }

  # Connections
  ADMIN_NEW = 'CONTRACTOR:ADD_NEW'
  ADMIN_EDIT = 'CONTRACTOR:EDIT'
  MENU = 'CONTRACTOR:MENU'
  LIST_ALL = 'CONTRACTOR:LIST_ALL'
  LIST_ALL_NEXT = 'CONTRACTOR:LIST_ALL_NEXT'
  LIST_ALL_PREV = 'CONTRACTOR:LIST_ALL_PREV'
  SELECT_FROM_LIST = 'CONTRACTOR:SELECT_FROM_LIST'
  VIEW = 'CONTRACTOR:VIEW'
  SAVE = 'CONTRACTOR:SAVE'
  GET_ID = 'CONTRACTOR:GET_ID'
  FILTER_LOCATION = 'CONTRACTOR:FILTER_LOCATION'

class ReportConst():
  ''' Constants and connections for ReportView. '''
  # Constants
  FORM_PARAM = 'REPORT:FORM'
  TABLE_PARAM = 'REPORT:TABLE'
  REPORT_PARAM = 'REPORT:REPORT'
  INPUT_PARAM = 'REPORT:INPUT'

  TABLE_HEADERS = {
    'id': 'ID',
    'task_id': 'TASK',
    'report_date': 'REPORT DATE',
    'approved': 'APPROVED',
    'task_type': 'TASK TYPE',
    'employee_name': 'EMPLOYEE',
    'building_registration': 'BUILDING',
  }

  # Connections
  ADMIN_NEW = 'REPORT:ADD_NEW'
  ADMIN_EDIT = 'REPORT:EDIT'
  ADMIN_ACTIVE = 'REPORT:LIST_ACTIVE'
  MENU = 'REPORT:MENU'
  LIST_ALL = 'REPORT:LIST_ALL'
  PAGING_NEXT = 'REPORT:LIST_ALL_NEXT'
  PAGING_PREV = 'REPORT:LIST_ALL_PREV'
  SELECT_FROM_LIST = 'REPORT:SELECT_FROM_LIST'
  VIEW = 'REPORT:VIEW'
  SAVE = 'REPORT:SAVE'
  GET_ID = 'REPORT:GET_ID'
  FILTER_EMPLOYEE = 'REPORT:FILTER_EMPLOYEE'
  FILTER_TASK = 'REPORT:FILTER_TASK'
  FILTER_CONTRACTOR = 'REPORT:FILTER_CONTRACTOR'
  FILTER_BUILDING = 'REPORT:FILTER_BUILDING'


class AccConst():
  ''' Constants and connections for AccessoryView. '''
  # Constants
  FORM_PARAM = 'ACCESSORY:FORM'
  TABLE_PARAM = 'ACCESSORY:TABLE'
  ACCESSORY_PARAM = 'ACCESSORY:ACCESSORY'
  INPUT_PARAM = 'INPUT:INPUT'

  TABLE_HEADERS = {
    'id': 'ID',
    'name': 'NAME',
    'description': 'DESCRIPTION',
    'state': 'STATE',
    'last_maintained': 'FIXED'
  }

  # Connections
  ADMIN_NEW = 'ACCESSORY:ADD_NEW'
  ADMIN_EDIT = 'ACCESSORY:EDIT'
  MENU = 'ACCESSORY:MENU'
  LIST_ALL = 'ACCESSORY:LIST_ALL'
  LIST_ALL_NEXT = 'ACCESSORY:LIST_ALL_NEXT'
  LIST_ALL_PREV = 'ACCESSORY:LIST_ALL_PREV'
  SELECT_FROM_LIST = 'ACCESSORY:SELECT_FROM_LIST'
  VIEW = 'ACCESSORY:VIEW'
  SAVE = 'ACCESSORY:SAVE'
  GET_ID = 'ACCESSORY:GET_ID'
  FILTER_BUILDING = 'ACCESSORY:FILTER_BUILDING'

class SearchConst():
  ''' Constants and connections for SearchView. '''
  # Constants

  # Connections
  MENU = 'SEARCH:MENU'
  EMPLOYEE_BY_LOCATION = 'SEARCH:EMPLOYEE_BY_LOCATION'
  BUILDING_BY_LOCATION = 'SEARCH:BUILDING_BY_LOCATION'
  EMPLOYEE_BY_ID = 'SEARCH:EMPLOYEE_BY_ID'
  BUILDING_BY_ID = 'SEARCH:BUILDING_BY_ID'
  TASK_BY_ID = 'SEARCH:TASK_BY_ID'
  TASK_BY_BUILDING = 'SEARCH:TASK_BY_BUILDING'
  TASK_BY_EMPLOYEE = 'SEARCH:TASK_BY_EMPLOYEE'
  REPORT_BY_BUILDING = 'SEARCH:REPORT_BY_BUILDING'
  REPORT_BY_EMPLOYEE = 'SEARCH:REPORT_BY_EMPLOYEE'
