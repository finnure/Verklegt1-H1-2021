from dl.filehandler import FileHandler


class AccessoryData():

  def __init__(self):
    self.headers = [
      'id',
      'building_id',
      'description',
      'state',
      'bought',
      'last_maintained',
      'tasks'
    ]
    self.__file = FileHandler('accessories.csv', self.headers)

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
    ''' Converts data to either a dict or an instance of Accessory '''
    pass

  def prepare(self, data):
    ''' Converts data to a format that file expects '''
