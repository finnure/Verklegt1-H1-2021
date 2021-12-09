from dlapi import DlApi
from utils import Helpers
from models.task import Task
from ui.form import Form

class TaskLogic():

  def __init__(self, dlapi: DlApi):
    self.dlapi = dlapi

  def new(self, form: Form):
    task = self.__parse_form(form)
    updated_task = self.dlapi.add_task(task)
    if task.recurring.lower() == 'y':
      next_date = Helpers.get_next_date(task.start_date, task.due_date, task.repeats_every)
      while next_date is not None:
        task.start_date = next_date
        self.dlapi.add_task(task)
        next_date = Helpers.get_next_date(task.start_date, task.due_date, task.repeats_every)
    return self.add_extras(updated_task)

  def update(self, form: Form):
    task = self.__parse_form(form)
    updated_task = self.dlapi.update_task(task.id, task)
    return self.add_extras(updated_task)

  def get(self, id: int):
    task = self.dlapi.get_one_task(id)
    return self.add_extras(task)

  def get_all(self):
    tasks = self.dlapi.get_all_tasks()
    return [self.add_extras(task) for task in tasks]

  def get_filtered(self, filter):
    tasks = self.dlapi.get_filtered_tasks(filter)
    return [self.add_extras(task) for task in tasks]

  def get_tasks_for_employee(self, id: int, statuses: 'list[str]' = None, from_date: str = None, to_date: str = None):
    filter = {'employee_id': id}
    tasks: 'list[Task]' = self.dlapi.get_filtered_tasks(filter)
    return self.apply_filters(tasks, statuses, from_date, to_date)

  def get_tasks_for_building(self, id: int, statuses: 'list[str]' = None, from_date: str = None, to_date: str = None):
    filter = {'building_id': id}
    tasks = self.get_filtered(filter)
    return self.apply_filters(tasks, statuses, from_date, to_date)

  def get_tasks_for_location(self, id: int, statuses: 'list[str]' = None, from_date: str = None, to_date: str = None):
    filter = {'location_id': id}
    tasks = self.get_filtered(filter)
    return self.apply_filters(tasks, statuses, from_date, to_date)

  def get_tasks_for_contractor(self, id: int, statuses: 'list[str]' = None, from_date: str = None, to_date: str = None):
    contractor = self.dlapi.get_one_contractor(id)
    c_filter = {'contractor_id': contractor.id}
    c_reports = self.dlapi.get_filtered_contractor_reports(c_filter) # contractor reports
    contractor.set_reports(c_reports)
    e_reports = [self.dlapi.get_one_employee_report(report) for report in c_reports] # employee reports
    tasks = [self.dlapi.get_one_task(rep.task_id) for rep in e_reports]
    return self.apply_filters(tasks, statuses, from_date, to_date)

  def apply_filters(self, tasks: 'list[Task]', statuses: 'list[str] | None', from_date: 'str | None', to_date: 'str | None'):
    if statuses is not None:
      statuses_lower = [stat.lower() for stat in statuses]
      tasks = [task for task in tasks if task.status.lower() in statuses_lower]
    if from_date is not None:
      if to_date is not None:
        # get time range
        tasks = [task for task in tasks if Helpers.date_between(from_date, to_date, task.start_date)]
      else:
        # get single day
        tasks = [task for task in tasks if Helpers.is_date(from_date, task.start_date)]
    return tasks


  def update_task_property(self, task: Task):
    task.modified = Helpers.get_current_date()
    updated_task = self.dlapi.update_task(task.id, task)
    return self.add_extras(updated_task)

  def calculate_task_cost(self, task: Task):
    return 0

  def add_extras(self, task: Task):
    filter = {'task_id': task.id}
    location = self.dlapi.get_one_location(task.location_id)
    building = self.dlapi.get_one_building(task.building_id)
    employee = self.dlapi.get_one_employee(task.employee_id)
    reports = self.dlapi.get_filtered_employee_reports(filter)
    task.set_location(location)
    task.set_building(building)
    task.set_employee(employee)
    task.set_reports(reports)
    return task

  def __parse_form(self, form: Form) -> Task:
    ''' Returns instance of Task if everything is ok. '''
    try:
      id = form['id']
      modified = Helpers.get_current_date()
    except StopIteration:
      id = 0
      modified = None
    return Task(
        id, 
        form['location_id'],
        form['building_id'],
        form['short_description'],
        form['type'],
        form['start_date'],
        form['due_date'],
        form['priority'],
        form['recurring'],
        form['status'],
        form['estimated_cost'],
        form['title'],
        form['repeats_every'],
        form['employee_id'],
        modified,
      )
