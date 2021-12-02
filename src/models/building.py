from typing import Type
from structs.accessory import Accessory
from structs.task import Task



class Building():

  def __init__(self, id: int, building_id: int, location_id: int,  description: str, state: str, task: list, \
    accessories: list, address: str, manager: str, reports: int, size: float, rooms: int, type: str) -> None:
    self.id = id
    self.building_id = building_id
    self.location_id = location_id
    self.description = description
    self.state = state
    self.task = []
    self.accessories = []
    self.address = address
    self.manager = manager
    self.reports = reports
    self.size = size
    self.rooms = rooms
    self.type = type
    
  def __str__(self) -> str:
    pass

  def add_accessory(self, accessory: Type[Accessory]) -> None:
    self.accessories.append(accessory)

  def add_task(self, task: Type[Task]) -> None:
    self.tasks.append(task)
  
  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id' : self.id,
      'building_id' : self.building_id,
      'location_id' : self.location_id,
      'description' : self.description,
      'state' : self.state,
      'task' : self.task, 
      'accessories' : self.accessories, 
      'address' : self.address, 
      'manager' : self.manager,
      'reports' : self.reports, 
      'size' : self.size, 
      'rooms' : self.rooms, 
      'type' : self.type
    }