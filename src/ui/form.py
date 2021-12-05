import utils

class Form():

  def __init__(self, fields: 'list[FormField]', instance = None):
    self.instance = instance
    self.form_fields = fields
    self.lines = sum([field.get_lines() for field in fields])
    self.spacing = max([len(field.name) for field in fields]) + 2


  def __getitem__(self, index):
    ''' Make form subscriptable. Form fields can be accessed using form[idx] '''
    if isinstance(index, slice):
      return self.form_fields[index.start:index.stop:index.step]
    return next(field.value for field in self.form_fields if field.key == index)

  def __iter__(self):
    ''' Make form iterable, can be used in a for loop with: for field in form '''
    return iter(self.form_fields)

class FormField():
  def __init__(self, 
                key: str, 
                name: str, 
                value: str,
                lines: int,
                cols: int,
                filter: str = utils.ALL_PRINTABLE,
                editable: bool = True,
                validators: list = None,
                options: str = None,
                border: bool = False):
    self.key = key
    self.name = name
    self.value = value
    self.lines = lines
    self.cols = cols
    self.filter = filter
    self.editable = editable
    self.validators = [] if validators is None else validators
    self.options = options
    self.border = border

  def get_lines(self):
    return self.lines + (2 if self.border else 0)

  def set_position(self, line: int, col: int):
    ''' Set postition where value begins. '''
    self.line = line + (1 if self.border else 0)
    self.col = col + (1 if self.border else 0)
