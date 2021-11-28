from typing import Type
from structs.report import EmployeeReport


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
    self.reports = []

  def __str__(self) -> str:
    pass

  def add_report(self, report: Type[EmployeeReport]) -> None:
    self.reports.append(report)
    