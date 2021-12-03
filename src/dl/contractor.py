from dl.filehandler import FileHandler
from models.contractor import Contractor



class ContractorData():

  def __init__(self, data_folder):
    self.headers = [
      'id',
      'location_id',
      'name',
      'contact',
      'phone',
      'opening_hours',
      'reports'
      'email',
      'rating',
      'speciality'
    ]
    self.data_folder = data_folder
    self.__file = FileHandler('contractors.csv', self.data_folder, self.headers)

  def add(self, contractor: Contractor) -> Contractor:
    ''' Add contractor to file. Gets next available id from csv file and 
    adds it to dict before adding to file. Returns contractor if successful. '''
    con = contractor.as_dict()
    con['id'] = self.__get_next_id()
    self.__file.add(con)
    return self.__parse(con)

  def update(self, id: int, contractor: Contractor) -> Contractor:
    ''' Updates contractor. Gets all data from file, replaces contractor
    that matches id and writes all data back to file. '''
    contractors = self.get_all()
    # Ternary with list comprehension. This replaces contractor in list if emp.id matches id
    updated_contractors = [contractor.as_dict() if con.id == id else con.as_dict() for con in contractors]
    self.__file.write(updated_contractors)
    return self.get_one(id)


  def delete(self, id: int) -> None:
    ''' Updates contractor. Gets all data from file, replaces contractor
    that matches id and writes all data back to file. '''
    contractors = self.get_all()
    # Ternary with list comprehension. This replaces contractor in list if emp.id matches id
    filtered_contractors = [con.as_dict() for con in contractors if con.id != id]
    self.__file.write(filtered_contractors)
    


  def get_all(self) -> 'list[Contractor]':
    ''' Get all contractors from file and return as list of Contractor instances. '''
    contractors = self.__file.read()
    return [self.__parse(contractor) for contractor in contractors]

  def get_one(self, id: int) -> 'Contractor | None':
    ''' Find Contractor matching the id specified. If no contractor is found, None is returned '''
    contractors = self.get_all()
    for contractor in contractors:
      if contractor.id == id:
        return contractor
    

  def get_filtered(self, filter: dict, partial_match: bool = False) -> 'list[Contractor]':
    ''' Get a list of Contractors matching filter specified.
    Filter should be a dict where key is the Contractor field to be matched and 
    value the value you're searching for. If filter includes more than one key, all keys
    need to match. If partial_match is true we do a partial match. Default is full match. '''
    contractors = self.get_all()
    for key, val in filter.items():
      if key in self.headers:
        if partial_match:
          filtered_contractors = [con for con in contractors if val in con[key]]
        else:
          filtered_contractors = [con for con in contractors if val == con[key]]
      else:
        # Wrong key in filter. Raise error
        raise KeyError(f'Invalid filter key for Contractor: {key}')
    return filtered_contractors
  

  def __parse(self, contractor: 'dict[str,str]') -> Contractor:
    ''' Creates and returns an instance of Contractor '''
    return Contractor(
        int(contractor['id']), 
        int(contractor['location_id']),
        contractor['name'],
        contractor['contact'],
        contractor['phone'],
        contractor['opening_hours'],
        contractor['reports'],
        contractor['email'],
        contractor['rating'],
        contractor['speciality]'],
      )
    
  def __get_next_id(self) -> int:
    ''' Finds max id and returns id+1 '''
    contractors = self.get_all()
    all_ids = [con.id for con in contractors]
    return max(all_ids) + 1
