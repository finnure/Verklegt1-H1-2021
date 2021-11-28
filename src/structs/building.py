from typing import Type
from structs.accessory import Accessory
from structs.task import Task



class Building():

  def __init__(self, id: int, location_id: int, free: bool, description: str, state: str) -> None:
    self.id = id
    self.location_id = location_id
    self.free = free
    self.description = description
    self.state = state
    self.accessories = []
    self.tasks = []
    
  def __str__(self) -> str:
    pass

  def add_accessory(self, accessory: Type[Accessory]) -> None:
    self.accessories.append(accessory)

  def add_task(self, task: Type[Task]) -> None:
    self.tasks.append(task)