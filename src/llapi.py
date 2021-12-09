from dlapi import DlApi
from bl.accessory import AccessoryLogic
from bl.building import BuildingLogic
from bl.contractor import ContractorLogic
from bl.employee import EmployeeLogic
from models.employee import Employee
from bl.location import LocationLogic
from bl.report import ReportLogic
from bl.task import TaskLogic
from models.task import Task
from ui.form import Form

class LlApi():
  def __init__(self):
    self.dlapi = DlApi()
    self.user: 'Employee | None' = None
    self.params = {}
    self.__init_logic()

  def __init_logic(self):
    self.accessory_logic = AccessoryLogic(self.dlapi)
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
    return self.params[key]
  
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

  def get_reports_for_building(self, id: int):
    return self.report_logic.get_reports_for_building(id)

  def get_accessories_for_building(self, id: int):
    return self.accessory_logic.get_filtered({'building_id': id})

  def get_buildings_by_location(self, id: int):
    return self.building_logic.get_filtered({'location_id': id})

  ##### Accessory methods ########

  def new_accessory(self, form: Form, building_id):
    return self.accessory_logic.new(form, building_id)

  def update_accessory(self, form: Form):
    return self.accessory_logic.update(form)

  def get_accessory(self, id: int):
    return self.accessory_logic.get(id)
  
  def get_all_accessories(self):
    return self.accessory_logic.get_all()

  def get_filtered_accessories(self, filter):
    return self.accessory_logic.get_filtered(filter)



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

  def get_employee_by_location(self, location_id: int):
    return self.employee_logic.get_employee_by_location(location_id)
  
  def get_reports_for_employee(self, filter):
    return self.report_logic.get_reports_for_employee(filter)

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

  def get_reports_for_task(self, task_id: int):
    return self.report_logic.get_reports_for_task(task_id)

  
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
  
  def update_task_property(self, task: Task):
    return self.task_logic.update_task_property(task)

  def calculate_task_cost(self, task: Task):
    return self.task_logic.calculate_task_cost(task)

  def get_tasks_for_building(self, id: int, statuses: 'list[str]' = None, from_date: str = None, to_date: str = None):
    return self.task_logic.get_tasks_for_building(id, statuses, from_date, to_date)
  
  def get_tasks_for_employee(self, id: int, statuses: 'list[str]' = None, from_date: str = None, to_date: str = None):
    return self.task_logic.get_tasks_for_employee(id, statuses, from_date, to_date)
  
  def get_tasks_for_location(self, id: int, statuses: 'list[str]' = None, from_date: str = None, to_date: str = None):
    return self.task_logic.get_tasks_for_location(id, statuses, from_date, to_date)
  
  def get_tasks_for_contractor(self, id: int, statuses: 'list[str]' = None, from_date: str = None, to_date: str = None):
    return self.task_logic.get_tasks_for_contractor(id, statuses, from_date, to_date)
  
