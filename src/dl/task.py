from dl.filehandler import FileHandler
from models.task import Task


class TaskData():

  def __init__(self, data_folder):
    self.headers = [
      'id',
      'short_description',
      'type',
      'estimated_cost',
      'start_date',
      'due_date',
      'modified',
      'priority',
      'building_id',
      'location_id',
      'employee_id',
      'recurring',
      'repeats_every',
      'title',
      'status',
    ]
    self.data_folder = data_folder
    self.__file = FileHandler('tasks.csv', self.data_folder, self.headers)

  def add(self, task: Task) -> Task:
    ''' Add task to file. Gets next available id from csv file and 
    adds it to dict before adding to file. Returns task if successful. '''
    tas = task.as_dict()
    tas['id'] = self.__get_next_id()
    self.__file.add(tas)
    return self.__parse(tas)

  def update(self, id: int, task: Task) -> Task:
    ''' Updates task. Gets all data from file, replaces task
    that matches id and writes all data back to file. '''
    tasks = self.get_all()
    # Ternary with list comprehension. This replaces task in list if tas.id matches id
    updated_tasks = [task.as_dict() if tas.id == id else tas.as_dict() for tas in tasks]
    self.__file.write(updated_tasks)
    return self.get_one(id)

  def delete(self, id: int) -> None:
    ''' Removes task from file. Gets all data from file, filters task
    that matches id from the list and writes all data back to file '''
    tasks = self.get_all()
    filtered_tasks = [tas.as_dict() for tas in tasks if tas.id != id]
    self.__file.write(filtered_tasks)

  def get_all(self) -> 'list[Task]':
    ''' Get all tasks from file and return as list of Task instances. '''
    tasks = self.__file.read()
    return [self.__parse(task) for task in sorted(tasks, key=lambda x: (x['priority'], x['start_date']))]

  def get_one(self, id: int) -> 'Task | None':
    ''' Find Task matching the id specified. If no task is found, None is returned '''
    tasks = self.get_all()
    for task in tasks:
      if task.id == id:
        return task

  def get_filtered(self, filter: dict, partial_match: bool = False) -> 'list[Task]':
    ''' Get a list of Tasks matching filter specified.
    Filter should be a dict where key is the Task field to be matched and 
    value the value you're searching for. If filter includes more than one key, all keys
    need to match. If partial_match is true we do a partial match. Default is full match. '''
    tasks = self.get_all()
    for key, val in filter.items():
      if key in self.headers:
        if partial_match:
          # Check if value is in field
          filtered_tasks = [task for task in tasks if str(val).lower() in str(getattr(task, key)).lower()]
        else:
          # Full match, check if value equals field
          filtered_tasks = [task for task in tasks if str(val).lower() == str(getattr(task, key)).lower()]
      else:
        # Wrong key in filter. Raise error
        raise KeyError(f'Invalid filter key for Task: {key}')
    return filtered_tasks

  def __parse(self, task: 'dict[str,str]') -> Task:
    ''' Creates and returns an instance of Task '''
    try:
      employee_id = int(task['employee_id'])
    except (ValueError, TypeError):
      employee_id = None
    try:
      priority = int(task['priority'])
      priority = ['', 'High', 'Medium', 'Low'][priority]
    except (ValueError, IndexError):
      priority = None
    try:
      rep = int(task['repeats_every'])
      rep = ['', 'Day', 'Week', '28 Days', 'Year'][rep]
    except (ValueError, IndexError):
      rep = task['repeats_every']
    return Task(
        int(task['id']), 
        int(task['location_id']),
        int(task['building_id']),
        task['short_description'],
        task['type'],
        task['start_date'],
        task['due_date'],
        priority,
        task['recurring'],
        task['status'],
        task['estimated_cost'],
        task['title'],
        rep,
        employee_id,
        task['modified']
      )

  def __get_next_id(self) -> int:
    ''' Finds max id and returns id+1 '''
    tasks = self.get_all()
    all_ids = [tas.id for tas in tasks]
    return max(all_ids) + 1
  