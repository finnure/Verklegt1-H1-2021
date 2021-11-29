from typing import Type
from structs.building import Building
from structs.contractor import Contractor

from structs.employee import Employee


class Location():

  def __init__(self, id: int, country: str, airport: str, phone: int, openinghours: str) -> None:
    self.id = id
    self.country = country
    self.airport = airport
    self.phone = phone
    self.openinghours = openinghours
    self.employees = []
    self.buildings = []
    self.contractors = []

  def __str__(self) -> str:
    pass

  def add_supervisor(self, employee: Type[Employee]) -> None:
    self.supervisor = employee
    self.employees.append(employee)

  def add_employee(self, employee: Type[Employee]) -> None:
    self.employees.append(employee)

  def add_building(self, building: Type[Building]) -> None:
    self.buildings.append(building)

  def add_contractor(self, contractor: Type[Contractor]):
    self.contractors.append(contractor)