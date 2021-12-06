from dlapi import DlApi
from bl.building import BuildingLogic
from bl.contractor import ContractorLogic
from bl.employee import EmployeeLogic
from models.employee import Employee
from bl.location import LocationLogic
from bl.report import ReportLogic
from bl.task import TaskLogic
from ui.form import Form

class LlApi():
  def __init__(self):
    self.dlapi = DlApi()
    self.user: 'Employee | None' = None
    self.params = {}
    self.__init_logic()

  def __init_logic(self):
    self.building_logic = BuildingLogic(self.dlapi)
    self.contractor_logic = ContractorLogic(self.dlapi)
    self.employee_logic = EmployeeLogic(self.dlapi)
    self.location_logic = LocationLogic(self.dlapi)
    self.report_logic = ReportLogic(self.dlapi)
    self.task_logic = TaskLogic(self.dlapi)

  ##### Exposed methods ########

  def set_logged_in_user(self, user: Employee) -> None:
    ''' Store logged in Employee object here so view classes can access it. '''
    self.user = user

  def clear_logged_in_user(self) -> None:
    ''' Logged in Employee set to none on logout. '''
    self.user = None

  def set_param(self, key: str, value) -> None:
    ''' Store params that other views might need to use. '''
    self.params.update({key: value})

  def get_param(self, key: str):
    ''' Get stored param and delete it from params. 
    Raises an error if no param is available for given key. '''
    if key not in self.params:
      raise KeyError(f'No data available for key {key}')
    return self.params.pop(key)
  
  ##### Building methods ########

  def new_building(self, form: Form):
    return self.building_logic.new(form, self.user.location_id)
  
  def update_building(self, form: Form):
    return self.building_logic.update(form)

  def get_building(self, id: int):
    return self.building_logic.get(id)
  
  def get_all_buildings(self):
    return self.building_logic.get_all()

  def get_filtered_buildings(self, filter):
    return self.building_logic.get_filtered(filter)
  
  def add_accessory_to_building(self, form: Form, building_id):
    return self.building_logic.add_accessory_to_building(form, building_id)

  def get_reports_for_building(self, id: int):
    return self.report_logic.get_filtered({'building_id': id})

  ##### Contractor methods ########

  def new_contractor(self, form: Form):
    return self.contractor_logic.new(form, self.user.location_id)
  
  def update_contractor(self, form: Form):
    return self.contractor_logic.update(form)

  def get_contractor(self, id: int):
    return self.contractor_logic.get(id)
  
  def get_all_contractors(self):
    return self.contractor_logic.get_all()

  def get_filtered_contractors(self, filter):
    return self.contractor_logic.get_filtered(filter)

  def get_contractor_rating(self, id: int):
    return self.contractor_logic.get_contractor_rating(id)
  
  def get_reports_for_contractor(self, id: int):
    return self.report_logic.get_filtered({'contractor_id': id})

  ##### Employee methods ########

  def new_employee(self, form: Form):
    return self.employee_logic.new(form, self.user.location_id)
  
  def update_employee(self, form: Form):
    return self.employee_logic.update(form)

  def get_employee(self, id: int):
    return self.employee_logic.get(id)
  
  def get_all_employees(self):
    return self.employee_logic.get_all()

  def get_employee_by_location(self, filter):
    return self.employee_logic.get_employee_by_location(filter)
  
  def get_reports_for_employee(self, filter):
    return self.employee_logic.get_reports_for_employee(filter)

  def get_active_tasks_for_user(self, id: int):
    return self.task_logic.get_active_tasks_for_employee(id)
  
  ##### Location methods ########

  def new_location(self, form: Form):
    return self.location_logic.new(form)
  
  def update_location(self, form: Form):
    return self.location_logic.update(form)

  def get_location(self, id: int):
    return self.location_logic.get(id)
  
  def get_all_locations(self):
    return self.location_logic.get_all()

  ##### Report methods ########

  def new_report(self, form: Form):
    return self.report_logic.new(form)
  
  def update_report(self, form: Form):
    return self.report_logic.update(form)

  def get_report(self, id: int):
    return self.report_logic.get(id)
  
  def get_all_reports(self):
    return self.report_logic.get_all()

  def get_filtered_reports(self, filter):
    return self.report_logic.get_filtered(filter)
  
  def add_contractor_to_report(self):
    return self.report_logic.add_contractor_to_report()
  
  ##### Task methods ########

  def new_task(self, form: Form):
    return self.task_logic.new(form)
  
  def update_task(self, form: Form):
    return self.task_logic.update(form)

  def get_task(self, id: int):
    return self.task_logic.get(id)
  
  def get_all_tasks(self):
    return self.task_logic.get_all()

  def get_filtered_tasks(self, filter):
    return self.task_logic.get_filtered(filter)
  
  def add_report_to_task(self):
    return self.task_logic.add_report_to_task()

  def update_task_state(self):
    return self.task_logic.update_task_state()

  def calculate_task_cost(self):
    return self.task_logic.calculate_task_cost()

