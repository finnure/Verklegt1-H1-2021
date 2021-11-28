from dl.filehandler import FileHandler


class BuildingData():

  def __init__(self, data_folder):
    self.headers = [
      'id',
      'location_id',
      'name',
      'description',
      'status',
      'state',
      'tasks',
      'accessories'
    ]
    self.data_folder = data_folder
    self.__file = FileHandler('buildings.csv', self.data_folder, self.headers)

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
    ''' Converts data to either a dict or an instance of Building '''
    pass

  def prepare(self, data):
    ''' Converts data to a format that file expects '''
    