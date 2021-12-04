class Report():

  def __init__(self, id: int,  report_date: str, approved: bool, task_type: str,\
    description: str, note: str, hours: float) -> None:
    self.id = id
    self.report_date = report_date
    self.approved = approved
    self.task_type = task_type
    self.description = description
    self.note = note
    self.hours = hours

  def __str__(self) -> str:
    pass

class ContractorReport(Report):

  def __init__(self, id: int, 
               report_date: str,
               approved: bool,
               task_type: str,
               description: str,
               note: str,
               hours: float,
               contractor_id: int, 
               employee_report_id: int, 
               contractor_fee: float, 
               contractor_rating: float) -> None:
    super().__init__(id, report_date, approved,task_type, description, note, hours)
    self.contractor_id = contractor_id
    self.employee_report_id = employee_report_id
    self.contractor_fee = contractor_fee
    self.contractor_rating = contractor_rating
  
class EmployeeReport(Report):

  def __init__(self, id: int,
               report_date: str,
               approved: bool,
               task_type: str,
               description: str,
               note: str,
               hours: float,
               employee_id: int,
               task_id: int,
               material_cost: float,
               labor_cost: float,
               total_cost: float) -> None:
    super().__init__(id, report_date, approved, task_type, description, note, hours)
    self.employee_id = employee_id
    self.task_id = task_id
    self.material_cost = material_cost
    self.labor_cost = labor_cost
    self.total_cost = total_cost
    self.contractor_reports = []

  def add_contractor_report(self, report: ContractorReport):
    self.contractor_reports.append(report)

def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id': self.id,
      'report_date': self.report_date, 
      'approved': self.approved, 
      'task_type': self.task_type,
      'description': self.description,
      'note': self.note,
      'hours': self.hours,
      'contractor_id': self.contractor_id,
      'employee_report_id': self.employee_report_id,
      'contractor_fee': self.contractor_fee,
      'contractor_rating': self.contractor_rating,
      'employee_id': self.employee_id, 
      'task_id': self.task_id, 
      'material_cost': self.material_cost, 
      'labor_cost': self.labor_cost, 
      'contractor_reports': self.contractor_reports
    }