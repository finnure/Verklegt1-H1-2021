from typing import Type
from dlapi import DlApi

class EmployeeLogic():

  def __init__(self, dlapi: Type[DlApi]) -> None:
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

  def get_reports_for_employee(filter):
    pass