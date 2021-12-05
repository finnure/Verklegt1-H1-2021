from dl.accessory import AccessoryData
from dl.building import BuildingData
from dl.contractor import ContractorData
from dl.contractorreport import ContractorReportData
from dl.employee import EmployeeData
from dl.employeereport import EmployeeReportData
from dl.location import LocationData
from dl.task import TaskData
from models.employee import Employee
from models.location import Location
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
    self.accessory_data.add()

  def update_accessory(self):
    self.accessory_data.update()

  def delete_accessory(self):
    self.accessory_data.delete()

  def get_all_accessories(self):
    self.accessory_data.get_all()

  def get_one_accessory(self, id):
    self.accessory_data.get_one(id)

  def get_filtered_accessories(self):
    self.accessory_data.get_filtered()

  ######## Building methods ############

  def add_building(self):
    self.building_data.add()

  def update_building(self):
    self.building_data.update()

  def delete_building(self):
    self.building_data.delete()

  def get_all_buildings(self):
    self.building_data.get_all()

  def get_one_building(self, id):
    self.building_data.get_one(id)

  def get_filtered_buildings(self):
    self.building_data.get_filtered()

  ######## Contractor methods ############
  
  def add_contractor(self):
    self.contractor_data.add()

  def update_contractor(self):
    self.contractor_data.update()

  def delete_contractor(self):
    self.contractor_data.delete()

  def get_all_contractors(self):
    self.contractor_data.get_all()

  def get_one_contractor(self, id):
    self.contractor_data.get_one(id)

  def get_filtered_contractors(self):
    self.contractor_data.get_filtered()

  ######## ContractorReport methods ############
  
  def add_contractor_report(self):
    self.contractor_report_data.add()

  def update_contractor_report(self):
    self.contractor_report_data.update()

  def delete_contractor_report(self):
    self.contractor_report_data.delete()

  def get_all_contractor_reports(self):
    self.contractor_report_data.get_all()

  def get_one_contractor_report(self, id):
    self.contractor_report_data.get_one(id)

  def get_filtered_contractor_reports(self):
    self.contractor_report_data.get_filtered()

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
    self.employee_report_data.add()

  def update_employee_report(self):
    self.employee_report_data.update()

  def delete_employee_report(self):
    self.employee_report_data.delete()

  def get_all_employee_reports(self):
    self.employee_report_data.get_all()

  def get_one_employee_report(self, id):
    self.employee_report_data.get_one(id)

  def get_filtered_employee_reports(self):
    self.employee_report_data.get_filtered()

  ######## Location methods ############
  
  def add_location(self):
    self.location_data.add()

  def update_location(self):
    self.location_data.update()

  def delete_location(self):
    self.location_data.delete()

  def get_all_locations(self) -> 'list[Location]':
    self.location_data.get_all()

  def get_one_location(self, id):
    self.location_data.get_one(id)

  def get_filtered_locations(self):
    self.location_data.get_filtered()

  ######## Task methods ############
  
  def add_task(self):
    self.task_data.add()

  def update_task(self):
    self.task_data.update()

  def delete_task(self):
    self.task_data.delete()

  def get_all_tasks(self):
    self.task_data.get_all()

  def get_one_task(self, id):
    self.task_data.get_one(id)

  def get_filtered_tasks(self):
    self.task_data.get_filtered()
