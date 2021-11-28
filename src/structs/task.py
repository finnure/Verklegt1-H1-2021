from typing import Type
from structs.report import EmployeeReport


class Task():

  def __init__(self, id: int, building_id: int, type: str, created: str, modified: str,
                finished: str, priority: str, recurring: str, state: str, estimate: int) -> None:
    self.id = id
    self.building_id = building_id
    self.type = type
    self.created = created
    self.modified = modified
    self.finished = finished
    self.priority = priority
    self.recurring = recurring
    self.state = state
    self.estimate = estimate
    self.reports = []

  def __str__(self) -> str:
    pass

  def add_report(self, report: Type[EmployeeReport]) -> None:
    self.reports.append(report)
