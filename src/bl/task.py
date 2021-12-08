from dlapi import DlApi
from utils import Helpers
from models.task import Task
from ui.form import Form

class TaskLogic():

  def __init__(self, dlapi: DlApi):
    self.dlapi = dlapi

  def new(self, form: Form, location_id: int, building_id: int):
    task = self.__parse_form(form, location_id, building_id)
    updated_task = self.dlapi.add_task(task)
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
    filter = {'building_id': id}
    tasks = self.get_filtered(filter)
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


  def add_report_to_task(self):
    pass
  
  def update_task_state(self):
    pass

  def calculate_task_cost(self):
    pass

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

  def __parse_form(self, form: Form, location_id: int = None, building_id: int = None) -> Task:
    ''' Returns instance of Task if everything is ok. '''
    try:
      id = form['id']
    except StopIteration:
      id = 0
    if building_id is None:
      building_id = form['building_id']
    if location_id is None:
      location_id = form['location_id']
    return Task(
        id, 
        location_id,
        building_id,
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
        form['modified'],
      )
