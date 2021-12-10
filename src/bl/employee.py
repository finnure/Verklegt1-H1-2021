from models.location import Location
from ui.form import Form
from dlapi import DlApi
from models.employee import Employee
from models.report import EmployeeReport

class EmployeeLogic():

  def __init__(self, dlapi: DlApi) -> None:
    self.dlapi = dlapi

  def new(self, form: Form, location_id: int) -> Employee:
    ''' Add new employee. Takes in a form and location id, converts the form to an instance
    of Employee and sends it to data layer for writing to file. Gets a new Employee object
    back that is loaded with extras and sent back to View Layer '''
    emp = self.__parse_form(form, location_id)
    employee = self.dlapi.add_employee(emp)
    return self.add_extras(employee)

  def update(self, form: Form) -> Employee:
    ''' Creates an instance of Employee from form and sends it to data layer for update.
    Returns updated Employee loaded with extras '''
    emp = self.__parse_form(form)
    employee = self.dlapi.update_employee(emp.id, emp)
    return self.add_extras(employee)

  def get(self, id: int) -> Employee:
    ''' Get one employee by id, loads it with extras and return it. Returns None if nothing was found '''
    employee = self.dlapi.get_one_employee(id)
    if employee is None:
      return
    return self.add_extras(employee)

  def get_all(self) -> 'list[Employee]':
    ''' Gets a list of all employees from data layer, loads it with extras and returns a list '''
    employees = self.dlapi.get_all_employees()
    return [self.add_extras(emp) for emp in employees]

  def get_employee_by_location(self, location_id: int) -> 'list[Employee]':
    ''' Get a list of employees filtered by location '''
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
