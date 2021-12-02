from dlapi import DlApi
from bl.building import BuildingLogic
from bl.contractor import ContractorLogic
from bl.employee import EmployeeLogic
from models.employee import Employee
from bl.location import LocationLogic
from bl.report import ReportLogic
from bl.task import TaskLogic

class LlApi():
  def __init__(self):
    self.dlapi = DlApi()
    self.user: 'Employee | None' = None
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
    self.user = user

  def clear_logged_in_user(self) -> None:
    self.user = None

  ##### Building methods ########

  def new_building(self):
    self.building_logic.new()
  
  def update_building(self):
    self.building_logic.update()

  def get_building(self, id):
    self.building_logic.get(id)
  
  def get_all_buildings(self):
    self.building_logic.get_all()

  def get_filtered_buildings(self, filter):
    self.building_logic.get_filtered(filter)
  
  def add_accessory_to_building(self):
    self.building_logic.add_accessory_to_building()

  def get_reports_for_building(self, filter):
    self.building_logic.get_reports_for_building(filter)

  ##### Contractor methods ########

  def new_contractor(self):
    self.contractor_logic.new()
  
  def update_contractor(self):
    self.contractor_logic.update()

  def get_contractor(self, id):
    self.contractor_logic.get(id)
  
  def get_all_contractors(self):
    self.contractor_logic.get_all()

  def get_filtered_contractors(self, filter):
    self.contractor_logic.get_filtered(filter)

  def get_contractor_rating(self, id):
    self.contractor_logic.get_contractor_rating(id)
  
  def get_reports_for_contractor(self, filter):
    self.contractor_logic.get_reports_for_contractor(filter)

  ##### Employee methods ########

  def new_employee(self):
    return self.employee_logic.new()
  
  def update_employee(self):
    return self.employee_logic.update()

  def get_employee(self, id):
    return self.employee_logic.get(id)
  
  def get_all_employees(self):
    return self.employee_logic.get_all()

  def get_employee_by_location(self, filter):
    return self.employee_logic.get_employee_by_location(filter)
  
  def get_reports_for_employee(self, filter):
    return self.employee_logic.get_reports_for_employee(filter)

  def get_active_tasks_for_user(self, id: int):
    return self.task_logic.get_filtered({'employee_id': id})
  
  ##### Location methods ########

  def new_location(self):
    self.location_logic.new()
  
  def update_location(self):
    self.location_logic.update()

  def get_location(self, id):
    self.location_logic.get(id)
  
  def get_all_locations(self):
    self.location_logic.get_all()

  def add_employee_to_location(self):
    self.location_logic.add_employee_to_location()

  ##### Report methods ########

  def new_report(self):
    self.report_logic.new()
  
  def update_report(self):
    self.report_logic.update()

  def get_report(self, id):
    self.report_logic.get(id)
  
  def get_all_reports(self):
    self.report_logic.get_all()

  def get_filtered_reports(self, filter):
    self.report_logic.get_filtered(filter)
  
  def add_contractor_to_report(self):
    self.report_logic.add_contractor_to_report()
  
  ##### Task methods ########

  def new_task(self):
    self.task_logic.new()
  
  def update_task(self):
    self.task_logic.update()

  def get_task(self, id):
    self.task_logic.get(id)
  
  def get_all_tasks(self):
    self.task_logic.get_all()

  def get_filtered_tasks(self, filter):
    self.task_logic.get_filtered(filter)
  
  def add_report_to_task(self):
    self.task_logic.add_report_to_task()

  def update_task_state(self):
    self.task_logic.update_task_state()

  def calculate_task_cost(self):
    self.task_logic.calculate_task_cost()

