from dl.filehandler import FileHandler


class EmployeeData():

  def __init__(self):
    self.headers = [
      'id',
      'name',
      'ssn',
      'address',
      'phone',
      'mobile',
      'email',
      'role'
    ]
    self.__file = FileHandler('employees.csv', self.headers)

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
    ''' Converts data to either a dict or an instance of Employee '''
    pass

  def prepare(self, data):
    ''' Converts data to a format that file expects '''
