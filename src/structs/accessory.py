class Accessory():
  
  def __init__(self, id: int, building_id: int, name: str, description: str,
               state: str, bought: str, last_maintained: str) -> None:
    self.id = id
    self.building_id = building_id
    self.name = name
    self.description = description
    self.state = state
    self.bought = bought
    self.last_maintained = last_maintained

  def __str__(self) -> str:
    return f'{self.name} - {self.description}'
