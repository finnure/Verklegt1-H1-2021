from models.location import Location
from ui.form import Form
from dlapi import DlApi
from models.employee import Employee
from models.report import EmployeeReport

class EmployeeLogic():

  def __init__(self, dlapi: DlApi) -> None:
    self.dlapi = dlapi

  def new(self, form: Form, location_id: int) -> Employee:
    ''' TODO '''
    emp = self.__parse_form(form, location_id)
    employee = self.dlapi.add_employee(emp)
    return self.add_extras(employee)

  def update(self, form: Form) -> Employee:
    ''' TODO '''
    emp = self.__parse_form(form)
    employee = self.dlapi.update_employee(emp.id, emp)
    return self.add_extras(employee)

  def get(self, id: int) -> Employee:
    ''' TODO '''
    employee = self.dlapi.get_one_employee(id)
    if employee is None:
      return
    return self.add_extras(employee)

  def get_all(self) -> 'list[Employee]':
    ''' TODO '''
    employees = self.dlapi.get_all_employees()
    return [self.add_extras(emp) for emp in employees]

  def get_employee_by_location(self, location_id: int) -> 'list[Employee]':
    ''' TODO '''
    filter = {'location_id': location_id}
    employees = self.dlapi.get_filtered_employees(filter)
    return [self.add_extras(emp) for emp in employees]


  def add_extras(self, employee: Employee) -> Employee:
    ''' Adds extra properties to employee and returns it. '''
    location = self.dlapi.get_one_location(employee.location_id)
    #reports = self.dlapi.get_filtered_employee_reports({'employee_id': employee.id})
    #tasks = self.dlapi.get_filtered_tasks({'employee_id': employee.id})
    employee.set_location(location)
    #employee.set_reports(reports)
    #employee.set_tasks(tasks)
    return employee

  def __parse_form(self, form: Form, location_id: int = None) -> Employee:
    ''' Returns instance of Employee if everything is ok. '''
    try:
      id = form['id']
      role = form['role']
    except StopIteration:
      # id and role missing from form, set defaults for new employee
      id = 0
      role = 'EMPLOYEE'
    if location_id is None:
      location_id = form['location_id']

    return Employee(
        id, 
        location_id,
        form['name'],
        form['ssn'],
        form['address'],
        form['phone'],
        form['mobile'],
        form['email'],
        role,
      )
