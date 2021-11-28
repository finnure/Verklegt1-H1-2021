class Form():

  def __init__(self):
    self.form_fields = []

  def add_form_field(self, name: str, value: str, value_type: str, line: int, col: int) -> None:
    ''' Adds a new form field to the form.
    Name is the property name for the field.
    Value holds current value if it exists.
    value_type can be one of: string, number, multiline, boolean, dropdown.
    line and col mark the spot where form field should appear.'''
    self.form_fields.append(FormField(name, value, value_type, line, col))

  def __getitem__(self, index):
    ''' Make form subscriptable. Form fields can be accessed using form[idx] '''
    if isinstance(index, slice):
      return self.form_fields[index.start:index.stop:index.step]
    return self.form_fields[index]

  def __iter__(self):
    ''' Make form iterable, can be used in a for loop with: for field in form '''
    return iter(self.form_fields)

class FormField():
  def __init__(self, name: str, value: str, value_type: str, line: int, col: int):
    self.name = name
    self.value = value
    self.value_type = value_type
    self.line = line
    self.col = col

  def __str__(self):
    return f'<{self.value_type}>{self.name} = {self.value} at {self.col}x{self.line}'
