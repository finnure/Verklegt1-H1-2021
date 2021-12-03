class Task():

  def __init__(self, id: int, building_id: int, accessory_id: int, short_description: str,  type: str, start_date: str,
                due_date: str, priority: str, recurring: str, repeats_every: str, status: str, estimated_cost: int,
                title: str, modified: str) -> None:
    self.id = id
    self.building_id = building_id
    self.accessory_id = accessory_id
    self.short_description = short_description
    self.type = type
    self.start_date = start_date
    self.due_date = due_date
    self.priority = priority
    self.recurring = recurring
    self.repeats_every = repeats_every
    self.status = status
    self.estimated_cost = estimated_cost
    self.title = title
    self.modified = modified

  def __str__(self) -> str:
    pass

  def as_dict(self) -> 'dict[str, str | int]':
    return {
      'id': self.id,
      'building_id': self.building_id, 
      'accessory_id': self.accessory_id, 
      'short_desription': self.short_description, 
      'type': self.type, 
      'start_date': self.start_date, 
      'due_date': self.due_date, 
      'priority': self.priority, 
      'recurring': self.recurring, 
      'repeats_every': self.repeats_every, 
      'status': self.status, 
      'estimated_cost': self.estimated_cost, 
      'title': self.title, 
      'modified': self.modified
    }