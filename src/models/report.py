class Report():

  def __init__(self, id: int, description: str, type: str, hours: int, cost: int) -> None:
    self.id = id
    self.description = description
    self.type = type
    self.hours = hours
    self.cost = cost

  def __str__(self) -> str:
    pass

class ContractorReport(Report):

  def __init__(self, id: int, contractor_id: int, employee_report_id: int,
                description: str, type: str, hours: int, cost: int, rating: int) -> None:
    super().__init__(id, description, type, hours, cost)
    self.contractor_id = contractor_id
    self.employee_report_id = employee_report_id
    self.rating = rating
    
class EmployeeReport(Report):

  def __init__(self, id: int, employee_id: int, task_id: int, description: str, 
                type: str, hours: int, cost: int) -> None:
    super().__init__(id, description, type, hours, cost)
    self.employee_id = employee_id
    self.task_id = task_id
    self.contractor_reports = []

  def add_contractor_report(self, report: ContractorReport):
    self.contractor_reports.append(report)
