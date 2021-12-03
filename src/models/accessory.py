class Accessory():
  
  def __init__(self, id: int, building_id: int, description: str,
               state: str, bought: str, last_maintained: str, active: bool) -> None:
    self.id = id
    self.building_id = building_id
    self.description = description
    self.state = state
    self.bought = bought
    self.last_maintained = last_maintained
    self.active = active

  def __str__(self) -> str:
    return f'{self.id} - {self.description}'

  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id': self.id,
      'building_id': self.building_id,
      'description': self.description,
      'state': self.state,
      'bought': self.bought,
      'last_maintained': self.last_maintained,
      'active': self.active
    }