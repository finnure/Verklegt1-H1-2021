#from typing_extensions import ParamSpecArgs
from utils import Validate, Filters
from ui.form import FormField

class Location():

  def __init__(self, id: int, country: str, city: str, airport: str, address: str, phone: int, openinghours: str, manager: str) -> None:
    self.id = id
    self.country = country
    self.city = city
    self.airport = airport
    self.address = address
    self.phone = phone
    self.openinghours = openinghours
    self.manager = manager
    self.employees = []
    self.buildings = []
    self.contractors = []

  def __str__(self) -> str:
    pass

  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id': self.id,
      'country': self.country,
      'city': self.city,
      'airport': self.airport,
      'address': self.address,
      'phone': self.phone,
      'openinghours': self.openinghours,
      'manager': self.manager,
      'employees': self.employees,
      'buildings': self.buildings,
      'contractors': self.contractors
    }

  @staticmethod
  def get_new_fields():
    return [
      FormField('country', 'COUNTRY', None, 1, 32, validators=[Validate.options], options='LOCATION'),
      FormField('city', 'CITY', None, 1, 15),
      FormField('airport', 'AIRPORT', None, 1, 10),
      FormField('address', 'ADDRESS', None, 1, 10),
      FormField('phone', 'PHONE NUMBER', None, 1, 32, Filters.PHONE, validators=[Validate.phone]),
      FormField('openinghours', 'OPENING HOURS', None, 1, 32),
      FormField('manager', 'MANAGER', None, 1, 32, validators=[Validate.min_length(5)])
    ]
  
  def get_edit_fields(self):
        return [
      FormField('id', 'ID', self.id, 1, 3, editable=False),
      FormField('country', 'COUNTRY', self.country, 1, 32, validators=[Validate.options], options='LOCATION'),
      FormField('city', 'CITY', self.city, 1, 15),
      FormField('airport', 'AIRPORT', self.airport, 1, 10),
      FormField('address', 'ADDRESS', self.address, 1, 10),
      FormField('phone', 'PHONE NUMBER', self.phone, 1, 32, Filters.PHONE, validators=[Validate.phone]),
      FormField('openinghours', 'OPENING HOURS', self.openinghours, 1, 32),
      FormField('manager', 'MANAGER', self.manager, 1, 32, validators=[Validate.min_length(5)])
    ]
