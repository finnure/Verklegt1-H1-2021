from typing import Type

from structs.report import ContractorReport


class Contractor():

  def __init__(self, id: int, location_id: int, name: str, contact: str, phone: int, openinghours: str, reports: list, \
    email: str, rating: int, speciality: str ) -> None:
    self.id = id
    self.location_id = location_id
    self.name = name
    self.contact = contact
    self.phone = phone
    self.openinghours = openinghours
    self.reports = []
    self.email = email
    self.rating = rating
    self.speciality = speciality

  def __str__(self) -> str:
    pass

  def add_report(self, report: Type[ContractorReport]) -> None:
    self.reports.append(report)
  
  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id': self.id,
      'location_id': self.location_id,
      'name': self.name, 
      'contact': self.contact, 
      'phone': self.phone, 
      'openinghours': self.openinghours, 
      'reports': self.reports, 
      'email': self.email, 
      'rating': self.rating, 
      'speciality': self.speciality
    }