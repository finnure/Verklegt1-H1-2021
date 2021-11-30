from typing import Type

class Employee():

  def __init__(self, id: int, location_id: int, name: str, ssn: int,
                address: str, phone: int, mobile: int, email: str, role: str) -> None:
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

  def as_dict(self) -> 'dict[str, str]':
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
