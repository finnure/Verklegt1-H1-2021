from dl.accessory import AccessoryData
from dl.building import BuildingData
from dl.contractor import ContractorData
from dl.contractorreport import ContractorReportData
from dl.employee import EmployeeData
from dl.employeereport import EmployeeReportData
from dl.location import LocationData
from dl.task import TaskData
from models.accessory import Accessory
from models.building import Building
from models.contractor import Contractor
from models.employee import Employee
from models.location import Location
from models.report import ContractorReport, EmployeeReport
from models.task import Task
class DlApi():

  def __init__(self):
    self.data_folder = 'data/'
    self.__init_data()

  def __init_data(self):
    self.accessory_data = AccessoryData(self.data_folder)
    self.building_data = BuildingData(self.data_folder)
    self.contractor_data = ContractorData(self.data_folder)
    self.contractor_report_data = ContractorReportData(self.data_folder)
    self.employee_data = EmployeeData(self.data_folder)
    self.employee_report_data = EmployeeReportData(self.data_folder)
    self.location_data = LocationData(self.data_folder)
    self.task_data = TaskData(self.data_folder)

  ######## Exposed methods ############

  ######## Accessory methods ############
  
  def add_accessory(self, accessory: Accessory):
    return self.accessory_data.add(accessory)

  def update_accessory(self, id: int, accessory: Accessory):
    return self.accessory_data.update(id, accessory)

  def delete_accessory(self, id: int):
    return self.accessory_data.delete(id)

  def get_all_accessories(self):
    return self.accessory_data.get_all()

  def get_one_accessory(self, id: int):
    return self.accessory_data.get_one(id)

  def get_filtered_accessories(self, filter):
    return self.accessory_data.get_filtered(filter)

  ######## Building methods ############

  def add_building(self, building: Building):
    return self.building_data.add(building)

  def update_building(self, id: int, building: Building):
    return self.building_data.update(id, building)

  def delete_building(self, id: int):
    return self.building_data.delete(id)

  def get_all_buildings(self):
    return self.building_data.get_all()

  def get_one_building(self, id: int):
    return self.building_data.get_one(id)

  def get_filtered_buildings(self, filter):
    return self.building_data.get_filtered(filter)

  ######## Contractor methods ############
  
  def add_contractor(self, contractor: Contractor):
    return self.contractor_data.add(contractor)

  def update_contractor(self, id: int, contractor: Contractor):
    return self.contractor_data.update(id, contractor)

  def delete_contractor(self, id: int):
    return self.contractor_data.delete(id)

  def get_all_contractors(self):
    return self.contractor_data.get_all()

  def get_one_contractor(self, id: int):
    return self.contractor_data.get_one(id)

  def get_filtered_contractors(self, filter):
    return self.contractor_data.get_filtered(filter)

  ######## ContractorReport methods ############
  
  def add_contractor_report(self, contractor_report: ContractorReport):
    return self.contractor_report_data.add(contractor_report)

  def update_contractor_report(self, id: int, contractor_report: ContractorReport):
    return self.contractor_report_data.update(id, contractor_report)

  def delete_contractor_report(self, id: int):
    return self.contractor_report_data.delete(id)

  def get_all_contractor_reports(self):
    return self.contractor_report_data.get_all()

  def get_one_contractor_report(self, id: int):
    return self.contractor_report_data.get_one(id)

  def get_filtered_contractor_reports(self, filter):
    return self.contractor_report_data.get_filtered(filter)

  ######## Employee methods ############
  
  def add_employee(self, employee: Employee) -> Employee:
    ''' Add employee to file. Gets next available id from csv file and 
    adds it to dict before adding to file. Returns employee if successful. '''
    return self.employee_data.add(employee)

  def update_employee(self, id: int, employee: Employee) -> Employee:
    ''' Updates employee. Gets all data from file, replaces employee
    that matches id and writes all data back to file. '''
    return self.employee_data.update(id, employee)

  def delete_employee(self, id: int) -> None:
    ''' Removes employee from file. Gets all data from file, filters employee
    that matches id from the list and writes all data back to file '''
    self.employee_data.delete(id)

  def get_all_employees(self) -> 'list[Employee]':
    ''' Get all employees from file and return as list of Employee instances. '''
    return self.employee_data.get_all()

  def get_one_employee(self, id: int) -> 'Employee | None':
    ''' Find Employee matching the id specified. If no employee is found, None is returned '''
    return self.employee_data.get_one(id)

  def get_filtered_employees(self, filter: dict, partial_match: bool = False) -> 'list[Employee]':
    ''' Get a list of Employees matching filter specified.
    Filter should be a dict where key is the Employee field to be matched and 
    value the value you're searching for. If filter includes more than one key, all keys
    need to match. If partial_match is true we do a partial match. Default is full match. '''
    return self.employee_data.get_filtered(filter, partial_match)

  ######## EmployeeReport methods ############
  
  def add_employee_report(self, employee_report: EmployeeReport):
    return self.employee_report_data.add(employee_report)

  def update_employee_report(self, id: int, employee_report: EmployeeReport):
    return self.employee_report_data.update(id, employee_report)

  def delete_employee_report(self, id: int):
    return self.employee_report_data.delete(id)

  def get_all_employee_reports(self):
    return self.employee_report_data.get_all()

  def get_one_employee_report(self, id: int):
    return self.employee_report_data.get_one(id)

  def get_filtered_employee_reports(self, filter):
    return self.employee_report_data.get_filtered(filter)

  ######## Location methods ############
  
  def add_location(self, location: Location) -> Location:
    return self.location_data.add(location)

  def update_location(self, id: int, location: Location) -> Location:
    return self.location_data.update(id, location)

  def delete_location(self,id: int) -> None:
    self.location_data.delete(id)

  def get_all_locations(self) -> 'list[Location]':
    return self.location_data.get_all()

  def get_one_location(self, id: int) -> 'Location | None':
    return self.location_data.get_one(id)

  def get_filtered_locations(self, filter: dict, partial_match: bool = False) -> 'list[Location]':
    return self.location_data.get_filtered(filter, partial_match)

  ######## Task methods ############
  
  def add_task(self, task: Task):
    return self.task_data.add(task)

  def update_task(self, id: int, task: Task):
    return self.task_data.update(id, task)

  def delete_task(self, id: int):
    return self.task_data.delete(id)

  def get_all_tasks(self):
    return self.task_data.get_all()

  def get_one_task(self, id: int):
    return self.task_data.get_one(id)

  def get_filtered_tasks(self, filter):
    return self.task_data.get_filtered(filter)
