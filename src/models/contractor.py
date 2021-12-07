from ui.form import FormField
from utils import Filters, Validate


class Contractor():

  def __init__(self, id: int,
              location_id: int, 
              name: str, 
              contact: str, 
              phone: int, 
              openinghours: str, 
              email: str, 
              speciality: str ) -> None:
    self.id = id
    self.location_id = location_id
    self.name = name
    self.contact = contact
    self.phone = phone
    self.openinghours = openinghours
    self.email = email
    self.speciality = speciality

  def __str__(self) -> str:
    return f'#{self.id} - {self.name} - {self.phone}'

  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id': self.id,
      'location_id': self.location_id,
      'name': self.name, 
      'contact': self.contact, 
      'phone': self.phone, 
      'openinghours': self.openinghours, 
      'email': self.email, 
      'speciality': self.speciality
    }

  @staticmethod
  def get_new_fields():
    return [
      FormField('name', 'NAME', None, 1, 32, validators=[Validate.required]),
      FormField('contact', 'CONTACT', None, 1, 32),
      FormField('phone', 'PHONE', None, 1, 32, Filters.PHONE, validators=[Validate.phone]),
      FormField('openinghours', 'OPENING HOURS', None, 1, 32),
      FormField('email', 'EMAIL', None, 1, 64, validators=[Validate.email]),
      FormField('speciality', 'SPECIALITY', None, 1, 32),
    ]

  def get_edit_fields(self):
    return [
      FormField('id', 'ID', self.id, 1, 3, editable=False),
      FormField('location_id', 'LOCATION', self.location_id, 1, 3, editable=False),
      FormField('name', 'NAME', self.name, 1, 32, validators=[Validate.required]),
      FormField('contact', 'CONTACT', self.contact, 1, 32),
      FormField('phone', 'PHONE', self.phone, 1, 32, Filters.PHONE, validators=[Validate.phone]),
      FormField('openinghours', 'OPENING HOURS', self.openinghours, 1, 32),
      FormField('email', 'EMAIL', self.email, 1, 64, validators=[Validate.email]),
      FormField('speciality', 'SPECIALITY', self.speciality, 1, 32),
    ]
