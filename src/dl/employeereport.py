from dl.filehandler import FileHandler
from models.report import EmployeeReport


class EmployeeReportData():

  def __init__(self, data_folder):
    self.headers = [
      'id',
      'task_id',
      'report_date',
      'approved',
      'employee_id',
      'hours',
      'material_cost',
      'labor_cost',
      'description',
      'note',
      ]
    
    self.data_folder = data_folder
    self.__file = FileHandler('employee_reports.csv', self.data_folder, self.headers)

  def add(self, employeereport: EmployeeReport) -> EmployeeReport:
    ''' Add Employee report to file. Gets next available id from csv file and 
    adds it to dict before adding to file. Returns employee report if successful. '''
    emp_rep = employeereport.as_dict()
    emp_rep['id'] = self.__get_next_id()
    self.__file.add(emp_rep)
    return self.__parse(emp_rep)

  def update(self, id: int, employeereport: EmployeeReport) -> EmployeeReport:
    ''' Updates employee reports. Gets all data from file, replaces employee report
    that matches id and writes all data back to file. '''
    employeereports = self.get_all()
    # Ternary with list comprehension. This replaces employeereport in list if emp_rep.id matches id
    updated_employeereport = [employeereport.as_dict() if emp_rep.id == id else emp_rep.as_dict() for emp_rep in employeereports]
    self.__file.write(updated_employeereport)
    return self.get_one(id)
  

  def delete(self, id: int) -> None:
    ''' Removes employee report from file. Gets all data from file, filters employee report
    that matches id from the list and writes all data back to file '''
    employeereports = self.get_all()
    filtered_employeereports = [emp_rep.as_dict() for emp_rep in employeereports if emp_rep.id != id]
    self.__file.write(filtered_employeereports)

  def get_all(self) -> 'list[EmployeeReport]':
    ''' Get all employee reports from file and return as list of EmployeeReport instances. '''
    employeereports = self.__file.read()
    return [self.__parse(emp_rep) for emp_rep in employeereports]


  def get_one(self, id) -> 'EmployeeReport | None':
    ''' Find employee report matching the id specified. If no employee report is found, None is returned '''
    employeereports = self.get_all()
    for employeereport in employeereports:
      if employeereport.id == id:
        return employeereport

  def get_filtered(self, filter: dict, partial_match: bool = False) -> 'list[EmployeeReport]':
    ''' Get a list of EnployeeReports matching filter specified.
    Filter should be a dict where key is the Employeereport field to be matched and 
    value the value you're searching for. If filter includes more than one key, all keys
    need to match. If partial_match is true we do a partial match. Default is full match. '''
    employeereports = self.get_all()
    for key, val in filter.items():
      if key in self.headers:
        if partial_match:
          filtered_employeereports = [emp_rep for emp_rep in employeereports if str(val).lower() in str(getattr(emp_rep, key)).lower()]
        else:
          filtered_emp_reployeereports = [emp_rep for emp_rep in employeereports if str(val).lower() == str(getattr(emp_rep, key)).lower()]
      else:
        # Wrong key in filter. Raise error
        raise KeyError(f'Invalid filter key for EmployeeReport: {key}')
    return filtered_employeereports

  def __parse(self, employeereport: 'dict[str, str]') -> EmployeeReport:
    ''' Creates and returns an instance of EmployeeReport '''
    return EmployeeReport(
        int(employeereport['id']), 
        int(employeereport['task_id']),
        employeereport['report_date'],
        employeereport['approved'],
        int(employeereport['employee_id']),
        float(employeereport['hours']),
        float(employeereport['material_cost']),
        float(employeereport['labor_cost']),
        employeereport['description'],
        employeereport['note']
      )

  def __get_next_id(self) -> int:
    ''' Finds max id and returns id+1 '''
    employeereport = self.get_all()
    all_ids = [emp_rep.id for emp_rep in employeereport]
    return max(all_ids) + 1