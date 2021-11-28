from dl.filehandler import FileHandler


class EmployeeReportData():

  def __init__(self):
    self.headers = [
      'id',
      'employee_id',
      'description',
      'status',
      'type',
      'hours',
      'cost',
      'contractor_reports'
    ]
    self.__file = FileHandler('employee_reports.csv', self.headers)

  def add(self):
    pass

  def update(self):
    pass

  def delete(self):
    pass

  def get_all(self):
    pass

  def get_one(self, id):
    pass

  def get_filtered(self, filter):
    pass

  def parse(self, data: list):
    ''' Converts data to either a dict or an instance of EmployeeReport '''
    pass

  def prepare(self, data):
    ''' Converts data to a format that file expects '''
