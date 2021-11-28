from typing import Type

from structs.report import ContractorReport


class Contractor():

  def __init__(self, id: int, location_id: int, name: str, contact: str, phone: int, openinghours: str) -> None:
    self.id = id
    self.location_id = location_id
    self.name = name
    self.contact = contact
    self.phone = phone
    self.openinghours = openinghours
    self.reports = []

  def __str__(self) -> str:
    pass

  def add_report(self, report: Type[ContractorReport]) -> None:
    self.reports.append(report)
    