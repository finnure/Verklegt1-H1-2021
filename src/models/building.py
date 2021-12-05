from utils import Validate, Filters
from ui.form import FormField

class Building():

  def __init__(self, id: int, 
              registration: int, 
              location_id: int,  
              description: str, 
              state: str,
              address: str, 
              size: float, 
              rooms: int, 
              type: str) -> None:
    self.id = id
    self.registration = registration
    self.location_id = location_id
    self.description = description
    self.state = state
    self.address = address
    self.size = size
    self.rooms = rooms
    self.type = type
    
  def __str__(self) -> str:
    return f'#{self.id} - {self.address} - {self.registration}'

  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id' : self.id,
      'registration' : self.registration,
      'location_id' : self.location_id,
      'description' : self.description,
      'state' : self.state,
      'address' : self.address, 
      'size' : self.size, 
      'rooms' : self.rooms, 
      'type' : self.type
    }

  @staticmethod
  def get_new_fields():
    return [
      FormField('registration', 'REGISTRATION ID', None, 1, 10, validators=[Validate.required]),
      FormField('location_id', 'LOCATION', None, 1, 3, validators=[Validate.options], options='LOCATION'),
      FormField('description', 'DESCRIPTION', None, 1, 64),
      FormField('state', 'STATE', None, 1, 64),
      FormField('address', 'ADDRESS', None, 1, 32),
      FormField('size', 'SIZE', None, 1, 10, Filters.FLOATS),
      FormField('rooms', 'ROOMS', None, 1, 5, Filters.NUMBERS),
      FormField('type', 'TYPE', None, 1, 15),
    ]

  def get_edit_fields(self):
    return [
      FormField('id', 'ID', self.id, 1, 3, editable=False),
      FormField('registration', 'REGISTRATION ID', self.registration, 1, 10, validators=[Validate.required]),
      FormField('location_id', 'LOCATION', self.location_id, 1, 3, validators=[Validate.options], options='LOCATION'),
      FormField('description', 'DESCRIPTION', self.description, 1, 64),
      FormField('state', 'STATE', self.state, 1, 64),
      FormField('address', 'ADDRESS', self.address, 1, 32),
      FormField('size', 'SIZE', self.size, 1, 10, Filters.FLOATS),
      FormField('rooms', 'ROOMS', self.rooms, 1, 5, Filters.NUMBERS),
      FormField('type', 'TYPE', self.type, 1, 15),
    ]
