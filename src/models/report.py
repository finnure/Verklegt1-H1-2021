from utils import Validate, Filters
from ui.form import FormField

class Report():

  def __init__(self, id: int,
              report_date: str,
              approved: bool,
              description: str,
              note: str,
              hours: float) -> None:
    self.id = id
    self.report_date = report_date
    self.approved = approved
    self.description = description
    self.note = note
    self.hours = hours

  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id': self.id,
      'report_date': self.report_date, 
      'approved': self.approved, 
      'description': self.description,
      'note': self.note,
      'hours': self.hours,
      'employee_name': self.employee.name
    }
  
  def add_employee(self, employee):
    self.employee = employee
    
  def add_task(self, task):
    self.task = task

class ContractorReport(Report):

  def __init__(self, id: int, 
               report_date: str,
               approved: bool,
               description: str,
               note: str,
               hours: float,
               contractor_id: int, 
               employee_report_id: int, 
               contractor_fee: float, 
               contractor_rating: float) -> None:
    super().__init__(id, report_date, approved,description, note, hours)
    self.contractor_id = contractor_id
    self.employee_report_id = employee_report_id
    self.contractor_fee = contractor_fee
    self.contractor_rating = contractor_rating

  def add_contractor(self, contractor):
    self.contractor = contractor
  
  def as_dict(self) -> 'dict[str, str | int]':
    report = super().as_dict()
    return report.update({
      'contractor_id': self.contractor_id,
      'employee_report_id': self.employee_report_id,
      'contractor_fee': self.contractor_fee,
      'contractor_rating': self.contractor_rating,
      'contractor_name': self.contractor.name
    })

  @staticmethod
  def get_new_fields():
    return [
      FormField('description', 'DESCRIPTION', None, 1, 64),
      FormField('note', 'NOTE', None, 1, 64),
      FormField('hours', 'HOURS', None, 1, 5, Filters.NUMBERS),
      FormField('contractor_fee', 'CONTRACTOR FEE', None, 1, 15, Filters.FLOATS),
    ]

class EmployeeReport(Report):

  def __init__(self, id: int,
               report_date: str,
               approved: bool,
               description: str,
               note: str,
               hours: float,
               employee_id: int,
               task_id: int,
               material_cost: float,
               labor_cost: float) -> None:
    super().__init__(id, report_date, approved, description, note, hours)
    self.employee_id = employee_id
    self.task_id = task_id
    self.material_cost = material_cost
    self.labor_cost = labor_cost

  def add_contractor_reports(self, reports: 'list[ContractorReport]'):
    self.contractor_reports = reports

  def as_dict(self) -> 'dict[str, str | int]':
    report = super().as_dict()
    return report.update({
      'employee_id': self.employee_id, 
      'task_id': self.task_id, 
      'material_cost': self.material_cost, 
      'labor_cost': self.labor_cost, 
    })

  @staticmethod
  def get_new_fields():
    return [
      FormField('description', 'DESCRIPTION', None, 1, 64),
      FormField('note', 'NOTE', None, 1, 64),
      FormField('hours', 'HOURS', None, 1, 5, Filters.NUMBERS),
      FormField('material_cost', 'MATERIAL COST', None, 1, 10, Filters.FLOATS),
      FormField('labor_cost', 'ROOMS', None, 1, 5, Filters.NUMBERS),
    ]
