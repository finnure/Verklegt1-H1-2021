from ui.form import FormField
from utils import Filters, Validate

class Task():

  def __init__(self, id: int, 
              location_id: int, 
              building_id: int, 
              short_description: str, 
              type: str, 
              start_date: str,
              due_date: str, 
              priority: str, 
              recurring: str, 
              status: str, 
              estimated_cost: int,
              title: str, 
              repeats_every: str = None, 
              employee_id: int = None, 
              modified: str = None) -> None:
    self.id = id
    self.location_id = location_id
    self.building_id = building_id
    self.employee_id = employee_id
    self.short_description = short_description
    self.type = type
    self.start_date = start_date
    self.due_date = due_date
    self.priority = priority
    self.recurring = recurring
    self.repeats_every = repeats_every
    self.status = status
    self.estimated_cost = estimated_cost
    self.title = title
    self.modified = modified

  def __str__(self) -> str:
    return f'#{self.id} - {self.type} - {self.status}'

  def set_location(self, location):
    self.location = location

  def set_building(self, building):
    self.building = building
    self.building_reg = building.registration

  def set_employee(self, employee):
    self.employee = employee
    self.employee_name = None if employee is None else employee.name

  def set_reports(self, reports: list):
    self.reports = reports
  
  def __getitem__(self, name: str):
    return self.as_dict()[name]

  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id': self.id,
      'location_id': self.location_id, 
      'building_id': self.building_id, 
      'employee_id': self.employee_id, 
      'short_desription': self.short_description, 
      'type': self.type, 
      'start_date': self.start_date, 
      'due_date': self.due_date, 
      'priority': self.priority, 
      'recurring': self.recurring, 
      'repeats_every': self.repeats_every, 
      'status': self.status, 
      'estimated_cost': self.estimated_cost, 
      'title': self.title, 
      'modified': self.modified
    }

  @staticmethod
  def get_new_fields():
    return [
      FormField('title', 'TITLE', None, 1, 64),
      FormField('short_desription', 'DESRIPTION', None, 1, 64, validators=[Validate.required]),
      FormField('type', 'TYPE', None, 1, 15),
      FormField('start_date', 'START DATE', None, 1, 15, Filters.DATE, validators=[Validate.date]),
      FormField('due_date', 'DUE DATE', None, 1, 15, Filters.DATE, validators=[Validate.date]),
      FormField('priority', 'PRIORITY', None, 1, 32),
      FormField('recurring', 'RECURRING', None, 1, 3),
      FormField('repeats_every', 'REPEATS EVERY', None, 1, 10),
      FormField('estimated_cost', 'ESTIMATED COST', None, 1, 32, Filters.NUMBERS),
    ]

  def get_edit_fields(self):
    return [
      FormField('id', 'ID', self.id, 1, 3, editable=False),
      FormField('location_id', 'LOCATION', self.location_id, 1, 3, editable=False),
      FormField('building_id', 'BUILDING', self.building_id, 1, 3, editable=False),
      FormField('title', 'TITLE', self.title, 1, 64),
      FormField('short_desription', 'DESRIPTION', self.short_description, 1, 64, validators=[Validate.required]),
      FormField('type', 'TYPE', self.type, 1, 15),
      FormField('start_date', 'START DATE', self.start_date, 1, 15, Filters.DATE, validators=[Validate.date]),
      FormField('due_date', 'DUE DATE', self.due_date, 1, 15, Filters.DATE, validators=[Validate.date]),
      FormField('priority', 'PRIORITY', self.priority, 1, 32),
      FormField('recurring', 'RECURRING', self.recurring, 1, 3),
      FormField('repeats_every', 'REPEATS EVERY', self.repeats_every, 1, 10),
      FormField('status', 'STATUS', self.status, 1, 10),
      FormField('estimated_cost', 'ESTIMATED COST', self.estimated_cost, 1, 32, Filters.NUMBERS),
    ]
