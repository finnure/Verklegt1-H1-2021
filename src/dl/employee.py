from dl.filehandler import FileHandler
from models.employee import Employee

class EmployeeData():

  def __init__(self, data_folder):
    self.headers = [
      'id',
      'location_id',
      'name',
      'ssn',
      'address',
      'phone',
      'mobile',
      'email',
      'role'
    ]
    self.data_folder = data_folder
    self.__file = FileHandler('employees.csv', self.data_folder, self.headers)

  def add(self, employee: Employee) -> Employee:
    ''' Add employee to file. Gets next available id from csv file and 
    adds it to dict before adding to file. Returns employee if successful. '''
    emp = employee.as_dict()
    emp['id'] = self.__get_next_id()
    self.__file.add(emp)
    return self.__parse(emp)

  def update(self, id: int, employee: Employee) -> Employee:
    ''' Updates employee. Gets all data from file, replaces employee
    that matches id and writes all data back to file. '''
    employees = self.get_all()
    # Ternary with list comprehension. This replaces employee in list if emp.id matches id
    updated_employees = [employee.as_dict() if emp.id == id else emp.as_dict() for emp in employees]
    self.__file.write(updated_employees)
    return self.get_one(id)

  def delete(self, id: int) -> None:
    ''' Removes employee from file. Gets all data from file, filters employee
    that matches id from the list and writes all data back to file '''
    employees = self.get_all()
    filtered_employees = [emp.as_dict() for emp in employees if emp.id != id]
    self.__file.write(filtered_employees)

  def get_all(self) -> 'list[Employee]':
    ''' Get all employees from file and return as list of Employee instances. '''
    employees = self.__file.read()
    return [self.__parse(employee) for employee in employees]

  def get_one(self, id: int) -> 'Employee | None':
    ''' Find Employee matching the id specified. If no employee is found, None is returned '''
    employees = self.get_all()
    for employee in employees:
      if employee.id == id:
        return employee

  def get_filtered(self, filter: dict, partial_match: bool = False) -> 'list[Employee]':
    ''' Get a list of Employees matching filter specified.
    Filter should be a dict where key is the Employee field to be matched and 
    value the value you're searching for. If filter includes more than one key, all keys
    need to match. If partial_match is true we do a partial match. Default is full match. '''
    employees = self.get_all()
    for key, val in filter.items():
      if key in self.headers:
        if partial_match:
          # Check if value is in field
          filtered_employees = [emp for emp in employees if str(val).lower() in str(getattr(emp, key)).lower()]
        else:
          # Full match, check if value equals field
          filtered_employees = [emp for emp in employees if str(val).lower() == str(getattr(emp, key)).lower()]
      else:
        # Wrong key in filter. Raise error
        raise KeyError(f'Invalid filter key for Employee: {key}')
    return filtered_employees

  def __parse(self, employee: 'dict[str,str]') -> Employee:
    ''' Creates and returns an instance of Employee '''
    return Employee(
        int(employee['id']), 
        int(employee['location_id']),
        employee['name'],
        employee['ssn'],
        employee['address'],
        employee['phone'],
        employee['mobile'],
        employee['email'],
        employee['role'],
      )

  def __get_next_id(self) -> int:
    ''' Finds max id and returns id+1 '''
    employees = self.get_all()
    all_ids = [emp.id for emp in employees]
    return max(all_ids) + 1