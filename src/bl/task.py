from dlapi import DlApi
from models.task import Task
from ui.form import Form

class TaskLogic():

  def __init__(self, dlapi: DlApi):
    self.dlapi = dlapi

  def new(self, form: Form, location_id: int, building_id: int):
    task = self.__parse_form(form, location_id, building_id)
    return self.dlapi.add_task(task)

  def update(self, form: Form):
    task = self.__parse_form(form)
    return self.dlapi.update_task(task.id, task)

  def get(self, id: int):
    return self.dlapi.get_one_task(id)

  def get_all(self):
    return self.dlapi.get_all_tasks()

  def get_filtered(self, filter):
    return self.dlapi.get_filtered_tasks(filter)

  def add_report_to_task(self):
    pass
  
  def update_task_state(self):
    pass

  def calculate_task_cost(self):
    pass

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
