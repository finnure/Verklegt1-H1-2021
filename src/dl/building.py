from dl.filehandler import FileHandler
from models.building import Building


class BuildingData():

  def __init__(self, data_folder):
    self.headers = [
      'id',
      'registration',
      'location_id',
      'description',
      'state',
      'address',
      'size',
      'rooms',
      'type'
    ]
    self.data_folder = data_folder
    self.__file = FileHandler('buildings.csv', self.data_folder, self.headers)

  def add(self, building: Building) -> Building:
    ''' Add building to file. Gets next available id from csv file and 
    adds it to dict before adding to file. Returns building if successful. '''
    build = building.as_dict()
    build['id'] = self.__get_next_id()
    self.__file.add(build)
    return self.__parse(build)
    
  def update(self, id: int, building: Building) -> Building:
    ''' Updates building. Gets all data from file, replaces building
    that matches id and writes all data back to file. '''
    buildings = self.get_all()
    # Ternary with list comprehension. This replaces building in list if build.id matches id
    updated_buildings = [building.as_dict() if build.id == id else build.as_dict() for build in buildings]
    self.__file.write(updated_buildings)
    return self.get_one(id)
    

  def delete(self, id: int) -> None:
    ''' Removes building from file. Gets all data from file, filters building
    that matches id from the list and writes all data back to file '''
    buildings = self.get_all()
    filtered_buildings = [build.as_dict() for build in buildings if build.id != id]
    self.__file.write(filtered_buildings)
    
    
  def get_all(self) -> 'list[Building]':
    ''' Get all buildings from file and return as list of Building instances. '''
    buildings = self.__file.read()
    return [self.__parse(building) for building in buildings]
  

  def get_one(self, id: int) -> 'Building | None':
    ''' Find Building matching the id specified. If no building is found, None is returned '''
    buildings = self.get_all()
    for building in buildings:
      if building.id == id:
        return building
  

  def get_filtered(self, filter: dict, partial_match: bool = False) -> 'list[Building]':
    ''' Get a list of Buildings matching filter specified.
    Filter should be a dict where key is the Building field to be matched and 
    value the value you're searching for. If filter includes more than one key, all keys
    need to match. If partial_match is true we do a partial match. Default is full match. '''
    buildings = self.get_all()
    for key, val in filter.items():
      if key in self.headers:
        if partial_match:
          # Check if value is in field
          filtered_buildings = [build for build in buildings if val in build[key]]
        else:
          # Full match, check if value equals field
          filtered_buildings = [build for build in buildings if val == build[key]]
      else:
        # Wrong key in filter. Raise error
        raise KeyError(f'Invalid filter key for Building: {key}')
    return filtered_buildings
  

  def __parse(self, building: 'dict[str,str]') -> Building:
    ''' Creates and returns an instance of Employee '''
    return Building(
        int(building['id']), 
        building['registration'],
        int(building['location_id']),
        building['description'],
        building['state'],
        building['address'],
        building['size'],
        building['rooms'],
        building['type']
      )
  
  
  def __get_next_id(self) -> int:
    ''' Finds max id and returns id+1 '''
    buildings = self.get_all()
    all_ids = [build.id for build in buildings]
    return max(all_ids) + 1
