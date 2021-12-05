from ui.form import Form
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

  def new(self, form: Form) -> Employee:
    ''' TODO '''
    emp = self.__parse_form(form)
    return self.dlapi.add_employee(emp)

  def update(self, employee: 'dict[str,str]') -> Employee:
    ''' TODO '''
    emp = self.__parse_form(employee, employee['location_id'])
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

  def __parse_form(self, form: Form) -> Employee:
    ''' Returns instance of Employee if everything is ok. '''
    try:
      id = form['id']
      role = form['role']
    except StopIteration:
      id = 0
      role = 'EMPLOYEE'

    return Employee(
        id, 
        form['location_id'],
        form['name'],
        form['ssn'],
        form['address'],
        form['phone'],
        form['mobile'],
        form['email'],
        role,
      )
