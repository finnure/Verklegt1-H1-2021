from utils import Validate, Filters
from ui.form import FormField
class Accessory():
  
  def __init__(self, id: int, 
              building_id: int, 
              name: str,
              description: str,
              state: str, 
              bought: str, 
              last_maintained: str) -> None:
    self.id = id
    self.building_id = building_id
    self.name = name
    self.description = description
    self.state = state
    self.bought = bought
    self.last_maintained = last_maintained

  def __str__(self) -> str:
    return f'{self.id} - {self.description}'

  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id': self.id,
      'name': self.name,
      'building_id': self.building_id,
      'description': self.description,
      'state': self.state,
      'bought': self.bought,
      'last_maintained': self.last_maintained,
    }

  def set_building(self, building):
    self.building = building

  def update_maintained(self, date: str):
    self.last_maintained = date

  @staticmethod
  def get_new_fields():
    return [
      FormField('building_id', 'BUILDING ID', None, 1, 3, editable=False),
      FormField('name', 'NAME', None, 1, 64),
      FormField('description', 'DESCRIPTION', None, 1, 64),
      FormField('state', 'STATE', None, 1, 10),
      FormField('bought', 'BOUGHT', None, 1, 10, Filters.DATE, validators=[Validate.date]),
      FormField('last_maintained', 'LAST MAINTAINED', None, 1, 10, Filters.DATE, validators=[Validate.date]),
    ]

  def get_edit_fields(self):
    return [
      FormField('id', 'ID', self.id, 1, 3, editable=False),
      FormField('building_id', 'BUILDING ID', self.building_id, 1, 3, editable=False),
      FormField('name', 'NAME', self.name, 1, 64),
      FormField('description', 'DESCRIPTION', self.description, 1, 64),
      FormField('state', 'STATE', self.state, 1, 10),
      FormField('bought', 'BOUGHT', self.bought, 1, 15, Filters.DATE, validators=[Validate.date]),
      FormField('last_maintained', 'LAST MAINTAINED', self.last_maintained, 1, 15, Filters.DATE, validators=[Validate.date]),
    ]
