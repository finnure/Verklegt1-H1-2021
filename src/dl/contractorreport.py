from dl.filehandler import FileHandler


class ContractorReportData():

  def __init__(self):
    self.headers = [
      'id',
      'contractor_id',
      'employee_report_id',
      'description',
      'status',
      'type',
      'hours',
      'cost',
      'rating'
    ]
    self.__file = FileHandler('contractor_reports.csv', self.headers)

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
    ''' Converts data to either a dict or an instance of ContractorReport '''
    pass

  def prepare(self, data):
    ''' Converts data to a format that file expects '''
