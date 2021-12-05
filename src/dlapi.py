from dl.accessory import AccessoryData
from dl.building import BuildingData
from dl.contractor import ContractorData
from dl.contractorreport import ContractorReportData
from dl.employee import EmployeeData
from dl.employeereport import EmployeeReportData
from dl.location import LocationData
from dl.task import TaskData
from models.building import Building
from models.employee import Employee
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
  
  def add_accessory(self):
    return self.accessory_data.add()

  def update_accessory(self):
    return self.accessory_data.update()

  def delete_accessory(self):
    return self.accessory_data.delete()

  def get_all_accessories(self):
    return self.accessory_data.get_all()

  def get_one_accessory(self, id):
    return self.accessory_data.get_one(id)

  def get_filtered_accessories(self):
    return self.accessory_data.get_filtered()

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
  
  def add_contractor(self):
    return self.contractor_data.add()

  def update_contractor(self):
    return self.contractor_data.update()

  def delete_contractor(self):
    return self.contractor_data.delete()

  def get_all_contractors(self):
    return self.contractor_data.get_all()

  def get_one_contractor(self, id):
    return self.contractor_data.get_one(id)

  def get_filtered_contractors(self):
    return self.contractor_data.get_filtered()

  ######## ContractorReport methods ############
  
  def add_contractor_report(self):
    return self.contractor_report_data.add()

  def update_contractor_report(self):
    return self.contractor_report_data.update()

  def delete_contractor_report(self):
    return self.contractor_report_data.delete()

  def get_all_contractor_reports(self):
    return self.contractor_report_data.get_all()

  def get_one_contractor_report(self, id):
    return self.contractor_report_data.get_one(id)

  def get_filtered_contractor_reports(self):
    return self.contractor_report_data.get_filtered()

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
  
  def add_employee_report(self):
    return self.employee_report_data.add()

  def update_employee_report(self):
    return self.employee_report_data.update()

  def delete_employee_report(self):
    return self.employee_report_data.delete()

  def get_all_employee_reports(self):
    return self.employee_report_data.get_all()

  def get_one_employee_report(self, id):
    return self.employee_report_data.get_one(id)

  def get_filtered_employee_reports(self):
    return self.employee_report_data.get_filtered()

  ######## Location methods ############
  
  def add_location(self):
    return self.location_data.add()

  def update_location(self):
    return self.location_data.update()

  def delete_location(self):
    return self.location_data.delete()

  def get_all_locations(self):
    return self.location_data.get_all()

  def get_one_location(self, id):
    return self.location_data.get_one(id)

  def get_filtered_locations(self):
    return self.location_data.get_filtered()

  ######## Task methods ############
  
  def add_task(self):
    return self.task_data.add()

  def update_task(self):
    return self.task_data.update()

  def delete_task(self):
    return self.task_data.delete()

  def get_all_tasks(self):
    return self.task_data.get_all()

  def get_one_task(self, id):
    return self.task_data.get_one(id)

  def get_filtered_tasks(self):
    return self.task_data.get_filtered()
