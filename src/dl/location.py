from dl.filehandler import FileHandler
from models.location import Location

class LocationData():

  def __init__(self, data_folder):
    self.headers = [
      'id',
      'country',
      'city',
      'airport',
      'address',
      'phone',
      'openinghours',
    ]
    self.data_folder = data_folder
    self.__file = FileHandler('locations.csv', self.data_folder, self.headers)

  def add(self, location: Location) -> Location:
    ''' Add location to file. Gets next available id from csv file and 
    adds it to dict before adding to file. Returns location if successful. '''
    loc = location.as_dict()
    loc['id'] = self.__get_next_id()
    self.__file.add(loc)
    return self.__parse(loc)

  def update(self, id: int, location: Location) -> Location:
    ''' Updates location. Gets all data from file, replaces location
    that matches id and writes all data back to file. '''
    locations = self.get_all()
    # Ternary with list comprehension. This replaces location in list if loc.id matches id
    updated_locations = [location.as_dict() if loc.id == id else loc.as_dict() for loc in locations]
    self.__file.write(updated_locations)
    return self.get_one(id)

  def delete(self, id: int) -> None:
    ''' Removes location from file. Gets all data from file, filters location
    that matches id from the list and writes all data back to file '''
    locations = self.get_all()
    filtered_locations = [loc.as_dict() for loc in locations if loc.id != id]
    self.__file.write(filtered_locations)

  def get_all(self) -> 'list[Location]':
    ''' Get all locations from file and return as list of Location instances. '''
    locations = self.__file.read()
    return [self.__parse(location) for location in locations]

  def get_one(self, id):
    ''' Find Location matching the id specified. If no location is found, None is returned '''
    locations = self.get_all()
    for location in locations:
      if location.id == id:
        return location

  def get_filtered(self, filter: dict, partial_match: bool = False) -> 'list[Location]':
    ''' Get a list of Locations matching filter specified.
    Filter should be a dict where key is the Location field to be matched and 
    value the value you're searching for. If filter includes more than one key, all keys
    need to match. If partial_match is true we do a partial match. Default is full match. '''
    locations = self.get_all()
    for key, val in filter.items():
      if key in self.headers:
        if partial_match:
          # Check if value is in field
          filtered_locations = [loc for loc in locations if val in loc[key]]
        else:
          # Full match, check if value equals field
          filtered_locations = [loc for loc in locations if val == loc[key]]
      else:
        # Wrong key in filter. Raise error
        raise KeyError(f'Invalid filter key for Location: {key}')
    return filtered_locations

  def __parse(self,  location: 'dict[str,str]') -> Location:
    ''' Creates and returns an instance of Location '''
    return Location(
        int(location['id']), 
        location['country'],
        location['city'],
        location['airport'],
        location['address'],
        location['phone'],
        location['openinghours'],
      )
  def __get_next_id(self) -> int:
    ''' Finds max id and returns id+1 '''
    employees = self.get_all()
    all_ids = [emp.id for emp in employees]
    return max(all_ids) + 1
