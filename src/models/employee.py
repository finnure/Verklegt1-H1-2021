from utils import Validate, Filters
from ui.form import FormField

class Employee():

  def __init__(self, id: int, 
              location_id: int, 
              name: str,
              ssn: str,
              address: str,
              phone: str,
              mobile: str,
              email: str,
              role: str = 'EMPLOYEE'
              ) -> None:
    self.id = id
    self.location_id = location_id
    self.name = name
    self.ssn = ssn
    self.address = address
    self.phone = phone
    self.mobile = mobile
    self.email = email
    self.role = role

  def __str__(self) -> str:
    return f'#{self.id} - {self.name} - {self.role}'

  def set_location(self, location) -> None:
    self.location = location
    self.location_city = location.city
    
  def set_reports(self, reports) -> None:
    self.reports = reports

  def set_tasks(self, tasks) -> None:
    self.tasks = tasks

  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id': self.id,
      'location_id': self.location_id,
      'name': self.name,
      'ssn': self.ssn,
      'address': self.address,
      'phone': self.phone,
      'mobile': self.mobile,
      'email': self.email,
      'role': self.role,
      'location_city': self.location_city,
    }

  @staticmethod
  def get_new_fields():
    return [
      FormField('name', 'NAME', None, 1, 32, validators=[Validate.min_length(5)]),
      FormField('ssn', 'SSN', None, 1, 15, validators=[Validate.ssn]),
      FormField('phone', 'PHONE', None, 1, 32, Filters.PHONE, validators=[Validate.phone]),
      FormField('mobile', 'MOBILE', None, 1, 32, Filters.PHONE, validators=[Validate.phone]),
      FormField('email', 'E-MAIL', None, 1, 64, validators=[Validate.email]),
      FormField('address', 'ADDRESS', None, 1, 64),
      FormField('location_id', 'COUNTRY', None, 1, 3, validators=[Validate.options], options='LOCATION'),
    ]

  def get_edit_fields(self):
    return [
      FormField('id', 'ID', self.id, 1, 3, editable=False),
      FormField('name', 'NAME', self.name, 1, 32, validators=[Validate.min_length(5)]),
      FormField('ssn', 'SSN', self.ssn, 1, 15, editable=False),
      FormField('phone', 'PHONE', self.phone, 1, 32, Filters.PHONE, validators=[Validate.phone]),
      FormField('mobile', 'MOBILE', self.mobile, 1, 32, Filters.PHONE, validators=[Validate.phone]),
      FormField('email', 'E-MAIL', self.email, 1, 64, validators=[Validate.email]),
      FormField('address', 'ADDRESS', self.address, 1, 64),
      FormField('location_id', 'COUNTRY', self.location_id, 1, 3, validators=[Validate.options], options='LOCATION'),
      FormField('role', 'ROLE', self.role, 1, 10, editable=False),
    ]
