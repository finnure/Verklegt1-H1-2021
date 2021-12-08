from dl.filehandler import FileHandler
from models.accessory import Accessory


class AccessoryData():

  def __init__(self, data_folder):
    self.headers = [
      'id',
      'building_id',
      'name',
      'description',
      'state',
      'bought',
      'last_maintained',
    ]
    self.data_folder = data_folder
    self.__file = FileHandler('accessories.csv', self.data_folder, self.headers)

  def add(self, accessory: Accessory) -> Accessory:
    ''' Add accessory to file. Gets next available id from csv file and 
    adds it to dict before adding to file. Returns accessory if successful. '''
    acc = accessory.as_dict()
    acc['id'] = self.__get_next_id()
    self.__file.add(acc)
    return self.__parse(acc)

  def update(self, id: int, accessory: Accessory) -> Accessory:
    ''' Updates accessory. Gets all data from file, replaces accessory
    that matches id and writes all data back to file. '''
    accessories = self.get_all()
    # Ternary with list comprehension. This replaces accessory in list if acc.id matches id
    updated_accessories = [accessory.as_dict() if acc.id == id else acc.as_dict() for acc in accessories]
    self.__file.write(updated_accessories)
    return self.get_one(id)

  def delete(self, id: int) -> None:
    ''' Removes accessory from file. Gets all data from file, filters accessory
    that matches id from the list and writes all data back to file '''
    accessories = self.get_all()
    filtered_accessorie = [acc.as_dict() for acc in accessories if acc.id != id]
    self.__file.write(filtered_accessorie)

  def get_all(self) -> 'list[Accessory]':
    ''' Get all accessories from file and return as list of Accessory instances. '''
    accessories = self.__file.read()
    return [self.__parse(accessory) for accessory in accessories]

  def get_one(self, id: int) -> 'Accessory | None':
    ''' Find Accessory matching the id specified. If no accessory is found, None is returned '''
    accessories = self.get_all()
    for accessory in accessories:
      if accessory.id == id:
        return accessory

  def get_filtered(self, filter: dict, partial_match: bool = False) -> 'list[Accessory]':
    ''' Get a list of Accessories matching filter specified.
    Filter should be a dict where key is the Accessory field to be matched and 
    value the value you're searching for. If filter includes more than one key, all keys
    need to match. If partial_match is true we do a partial match. Default is full match. '''
    accessories = self.get_all()
    for key, val in filter.items():
      if key in self.headers:
        if partial_match:
          # Check if value is in field
          filtered_accessories = [acc for acc in accessories if str(val).lower() in str(getattr(acc, key)).lower()]
        else:
          # Full match, check if value equals field
          filtered_accessories = [acc for acc in accessories if str(val).lower() == str(getattr(acc, key)).lower()]
      else:
        # Wrong key in filter. Raise error
        raise KeyError(f'Invalid filter key for Accessory: {key}')
    return filtered_accessories

  def __parse(self, accessory: 'dict[str,str]') -> Accessory:
    ''' Creates and returns an instance of Accessory '''
    return Accessory(
        int(accessory['id']), 
        int(accessory['building_id']),
        accessory['name'],
        accessory['description'],
        accessory['state'],
        accessory['bought'],
        accessory['last_maintained'],
      )


  def __get_next_id(self) -> int:
    ''' Finds max id and returns id+1 '''
    accessories = self.get_all()
    all_ids = [acc.id for acc in accessories]
    return max(all_ids) + 1

