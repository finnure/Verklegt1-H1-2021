class GlobalConst():
  ''' Global constants and connections. '''
  # Constants

  # Connections
  BACK = 'GLOBAL:BACK'
  MAIN_MENU = 'MENU:MENU'

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


class EmpConst():
  ''' Constants and connections for EmployeeView. '''
  # Constants
  FORM_PARAM = 'EMPLOYEE:FORM'
  TABLE_PARAM = 'EMPLOYEE:TABLE'
  EMPLOYEE_PARAM = 'EMPLOYEE:EMPLOYEE'

  # Connections
  ADMIN_NEW = 'EMPLOYEE:ADD_NEW'
  ADMIN_EDIT = 'EMPLOYEE:EDIT'
  MENU = 'EMPLOYEE:MENU'
  FILTER_LOCATION = 'EMPLOYEE:FILTER_LOCATION'
  LIST_ALL = 'EMPLOYEE:LIST_ALL'
  LIST_ALL_NEXT = 'EMPLOYEE:LIST_ALL_NEXT'
  LIST_ALL_PREV = 'EMPLOYEE:LIST_ALL_PREV'
  LIST_TASKS = 'EMPLOYEE:LIST_TASKS'
  LIST_REPORTS = 'EMPLOYEE:LIST_REPORTS'
  SELECT_FROM_LIST = 'EMPLOYEE:SELECT_FROM_LIST'
  VIEW = 'EMPLOYEE:VIEW'
  SAVE = 'EMPLOYEE:SAVE'
  GET_ID = 'EMPLOYEE:GET_ID'

class LocConst():
  ''' Constants and connections for LocationView. '''
  # Constants
  FORM_PARAM = 'LOCATION:FORM'
  TABLE_PARAM = 'LOCATION:TABLE'
  LOCATION_PARAM = 'LOCATION:LOCATION'

  # Connections
  MENU = 'LOCATION:MENU'
  ADMIN_NEW = 'LOCATION:ADD_NEW'
  ADMIN_EDIT = 'LOCATION:EDIT'
  MENU = 'LOCATION:MENU'
  FILTER_LOCATION = 'LOCATION:FILTER_LOCATION'
  LIST_ALL = 'LOCATION:LIST_ALL'
  LIST_ALL_NEXT = 'LOCATION:LIST_ALL_NEXT'
  LIST_ALL_PREV = 'LOCATION:LIST_ALL_PREV'
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

  # Connections
  MENU = 'TASK:MENU'

class BuildConst():
  ''' Constants and connections for BuildingView. '''
  # Constants

  # Connections
  MENU = 'BUILDING:MENU'

class ContrConst():
  ''' Constants and connections for ContractorView. '''
  # Constants

  # Connections
  MENU = 'CONTRACTOR:MENU'

class ReportConst():
  ''' Constants and connections for ReportView. '''
  # Constants

  # Connections
  MENU = 'REPORT:MENU'

class AccConst():
  ''' Constants and connections for AccessoryView. '''
  # Constants

  # Connections
  MENU = 'ACCESSORY:MENU'

