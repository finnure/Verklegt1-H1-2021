from ui.constants import Styles
from ui.form import FormField
from ui.menu import Menu
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
    self.reports = []
    self.building_reg = ''

  def __str__(self) -> str:
    return f'TASK - T{self.id}'

  def get_priority_for_csv(self):
    return ['', 'High', 'Medium', 'Low'].index(self.priority)

  def get_repeats_for_csv(self):
    return ['', 'Day', 'Week', '28 Days', 'Year'].index(self.repeats_every)

  def set_location(self, location):
    self.location = location

  def set_building(self, building):
    self.building = building
    self.building_reg = building.registration

  def set_employee(self, employee):
    self.employee = employee
    self.employee_name = '' if employee is None else employee.name

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
      'title': self.title, 
      'short_description': self.short_description, 
      'type': self.type, 
      'start_date': self.start_date, 
      'due_date': self.due_date, 
      'priority': self.get_priority_for_csv(), 
      'recurring': self.recurring, 
      'repeats_every': self.get_repeats_for_csv(), 
      'estimated_cost': self.estimated_cost, 
      'status': self.status, 
      'modified': self.modified
    }

  @staticmethod
  def get_priority_menu(line = 0):
    menu = Menu(line, 0)
    menu.add_menu_item('1', 'HIGH')
    menu.add_menu_item('2', 'MEDIUM')
    menu.add_menu_item('3', 'LOW')
    return menu

  @staticmethod
  def get_recurring_menu(line = 0):
    menu = Menu(line, 0)
    menu.add_menu_item('Y', 'YES')
    menu.add_menu_item('N', 'NO')
    return menu

  @staticmethod
  def get_repeats_menu(line = 0):
    menu = Menu(line, 0)
    menu.add_menu_item('1', 'DAILY')
    menu.add_menu_item('2', 'WEEKLY')
    menu.add_menu_item('3', 'EVERY 28 DAYS')
    menu.add_menu_item('4', 'YEARLY')
    return menu



  @staticmethod
  def get_new_fields():
    return [
      FormField('title', 'TITLE', None, 1, 64),
      FormField('short_description', 'DESRIPTION', None, 1, 64, validators=[Validate.required]),
      FormField('type', 'TYPE', None, 1, 15),
      FormField('start_date', 'START DATE', None, 1, 10, Filters.DATE, validators=[Validate.date, Validate.required]),
      FormField('due_date', 'END DATE', None, 1, 10, Filters.DATE, validators=[Validate.date, Validate.required]),
      FormField('priority', 'PRIORITY', None, 1, 1, '123', options=Task.get_priority_menu(5)),
      FormField('recurring', 'RECURRING', None, 1, 1, 'YyNn', options=Task.get_recurring_menu(5)),
      FormField('repeats_every', 'REPEATS EVERY', None, 1, 1, '1234', options=Task.get_repeats_menu(5)),
      FormField('estimated_cost', 'ESTIMATED COST', None, 1, 10, Filters.NUMBERS),
      FormField('status', 'STATUS', 'Available', 1, 3, editable=False),
      FormField('location_id', 'LOCATION ID', None, 1, 3, editable=False),
      FormField('building_id', 'BUILDING ID', None, 1, 3, editable=False),
      FormField('employee_id', 'EMPLOYEE ID', None, 1, 3, editable=False),
    ]

  def get_edit_fields(self):
    return [
      FormField('id', 'ID', self.id, 1, 3, editable=False),
      FormField('location_id', 'LOCATION ID', self.location_id, 1, 3, editable=False),
      FormField('building_id', 'BUILDING ID', self.building_id, 1, 3, editable=False),
      FormField('employee_id', 'EMPLOYEE ID', self.employee_id, 1, 3, editable=False),
      FormField('title', 'TITLE', self.title, 1, 64),
      FormField('short_description', 'DESRIPTION', self.short_description, 1, 64, validators=[Validate.required]),
      FormField('type', 'TYPE', self.type, 1, 15),
      FormField('start_date', 'START DATE', self.start_date, 1, 10, Filters.DATE, validators=[Validate.date]),
      FormField('due_date', 'END DATE', self.due_date, 1, 10, Filters.DATE, validators=[Validate.date]),
      FormField('priority', 'PRIORITY', self.priority, 1, 1, '123', options=Task.get_priority_menu(6)),
      FormField('recurring', 'RECURRING', self.recurring, 1, 1, editable=False),
      FormField('repeats_every', 'REPEATS EVERY', self.repeats_every, 1, 1, editable=False),
      FormField('estimated_cost', 'ESTIMATED COST', self.estimated_cost, 1, 10, Filters.NUMBERS),
      FormField('status', 'STATUS', self.status, 1, 10, editable=False),
    ]
