import utils
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
    return f'Name: {self.name}\nEmail: {self.email}\nPhone: {self.phone}'

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
    }

  @staticmethod
  def get_new_fields():
    return [
      FormField('name', 'NAME', None, 1, 32),
      FormField('ssn', 'SSN', None, 1, 15, validator=utils.validate_ssn),
      FormField('phone', 'PHONE', None, 1, 10, utils.PHONE, validator=utils.validate_phone),
      FormField('mobile', 'MOBILE', None, 1, 10, utils.PHONE, validator=utils.validate_phone),
      FormField('email', 'E-MAIL', None, 1, 32, validator=utils.validate_phone),
      FormField('address', 'ADDRESS', None, 1, 32),
      FormField('location_id', 'COUNTRY', None, 1, 1, options='LOCATION'),
      FormField('role', 'ROLE', None, 1, 1, options='ROLE')
    ]

  def get_edit_fields(self):
    return [
      FormField('id', 'ID', self.id, 1, 3, editable=False),
      FormField('name', 'NAME', self.name, 1, 32),
      FormField('ssn', 'SSN', self.ssn, 1, 15, editable=False),
      FormField('phone', 'PHONE', self.phone, 1, 10, utils.PHONE, validator=utils.validate_phone),
      FormField('mobile', 'MOBILE', self.mobile, 1, 10, utils.PHONE, validator=utils.validate_phone),
      FormField('email', 'E-MAIL', self.email, 1, 32, validator=utils.validate_phone),
      FormField('address', 'ADDRESS', self.address, 1, 32),
      FormField('location_id', 'COUNTRY', self.location_id, 1, 1, options='LOCATION'),
      FormField('role', 'ROLE', self.role, 1, 1, options='ROLE')
    ]
