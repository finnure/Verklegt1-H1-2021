from typing import Type
from dlapi import DlApi

class BuildingLogic():

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

  def add_accessory_to_building(self):
    pass

  def get_reports_for_building(self, filter):
    pass
