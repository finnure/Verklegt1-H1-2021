from typing import Type
from dlapi import DlApi

class TaskLogic():

  def __init__(self, dlapi: Type[DlApi]):
    self.dlapi = dlapi

  def new(self):
    pass

  def update(self):
    pass

  def get(self, id):
    pass

  def get_all(self):
    pass

  def get_filtered(self, filter):
    pass

  def add_report_to_task(self):
    pass
  
  def update_task_state(self):
    pass

  def calculate_task_cost(self):
    pass
