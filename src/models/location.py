#from typing_extensions import ParamSpecArgs
from utils import Validate, Filters
from ui.form import FormField

class Location():

  def __init__(self, id: int, country: str, city: str, airport: str, address: str, phone: int, opening_hours: str, manager_id: int) -> None:
    self.id = id
    self.country = country
    self.city = city
    self.airport = airport
    self.address = address
    self.phone = phone
    self.opening_hours = opening_hours
    self.manager_id = manager_id

  def __str__(self) -> str:
    return '#{}  {}, {}'.format(str(self.id),self.city,self.country)

  def set_buildings(self, buildings):
    self.buildings = buildings

  def set_manager(self, manager):
    self.manager = manager
    self.manager_name = manager.name

  def set_employees(self, employees):
    self.employees = employees

  def set_contractors(self, contractors):
    self.contractors = contractors

  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id': self.id,
      'country': self.country,
      'city': self.city,
      'airport': self.airport,
      'address': self.address,
      'phone': self.phone,
      'opening_hours': self.opening_hours,
      'manger_id': self.manager_id
    }

  @staticmethod
  def get_new_fields():
    return [
      FormField('country', 'COUNTRY', None, 1, 32, validators=[Validate.options], options='LOCATION'),
      FormField('city', 'CITY', None, 1, 32),
      FormField('airport', 'AIRPORT', None, 1, 64),
      FormField('address', 'ADDRESS', None, 1, 64),
      FormField('phone', 'PHONE NUMBER', None, 1, 32, Filters.PHONE, validators=[Validate.phone]),
      FormField('opening_hours', 'OPENING HOURS', None, 1, 32),
    ]
  
  def get_edit_fields(self):
        return [
      FormField('id', 'ID', self.id, 1, 3, editable=False),
      FormField('country', 'COUNTRY', self.country, 1, 32, validators=[Validate.options], options='LOCATION'),
      FormField('city', 'CITY', self.city, 1, 32),
      FormField('airport', 'AIRPORT', self.airport, 1, 64),
      FormField('address', 'ADDRESS', self.address, 1, 64),
      FormField('phone', 'PHONE NUMBER', self.phone, 1, 32, Filters.PHONE, validators=[Validate.phone]),
      FormField('opening_hours', 'OPENING HOURS', self.opening_hours, 1, 32),
    ]
