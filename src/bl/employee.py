import utils
from dlapi import DlApi
from models.employee import Employee
from models.report import EmployeeReport

class EmployeeLogic():

  def __init__(self, dlapi: DlApi) -> None:
    self.dlapi = dlapi
    self.required_headers = [
      'name',
      'ssn',
      'address',
      'phone',
      'mobile',
      'email',
      'role'
    ]

  def new(self, employee: 'dict[str,str]') -> Employee:
    ''' TODO '''
    emp = self.__validate(employee, 1)
    return self.dlapi.add_employee(emp)

  def update(self, employee: 'dict[str,str]') -> Employee:
    ''' TODO '''
    emp = self.__validate(employee, employee['location_id'])
    return self.dlapi.update_employee(emp.id, emp)

  def get(self, id: int) -> Employee:
    ''' TODO '''
    return self.dlapi.get_one_employee(id)

  def get_all(self) -> 'list[Employee]':
    ''' TODO '''
    return self.dlapi.get_all_employees()

  def get_employee_by_location(self, location_id: int) -> 'list[Employee]':
    ''' TODO '''
    filter = {'location_id': location_id}
    return self.dlapi.get_filtered_employees(filter)

  def get_reports_for_employee(self, id: int) -> 'list[EmployeeReport]':
    ''' TODO '''
    pass

  def __validate(self, employee: 'dict[str,str]', location_id: int) -> Employee:
    ''' Validates that data is correct. Throws error if it's not.
    Returns instance of Employee if everything is ok. '''
    utils.validate_headers(self.required_headers, employee.keys())
    utils.validate_phone(employee['mobile'])
    utils.validate_phone(employee['phone'])
    utils.validate_email(employee['email'])
    if not 'id' in employee:
      employee['id'] = 0

    return Employee(
        employee['id'], 
        location_id,
        employee['name'],
        employee['ssn'],
        employee['address'],
        employee['phone'],
        employee['mobile'],
        employee['email'],
        employee['role'],
      )
