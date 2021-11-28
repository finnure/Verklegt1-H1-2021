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

  def get_form_field(self, index: int):
    ''' Returns form field at index '''
    if len(self.form_fields) > index:
      return self.form_fields[index]

  def __iter__(self):
    self.n = 0
    return self

  def __next__(self):
    if self.n < len(self.form_fields):
      field = self.form_fields[self.n]
      self.n += 1
      return field
    else:
      raise StopIteration


class FormField():
  def __init__(self, name: str, value: str, value_type: str, line: int, col: int):
    self.name = name
    self.value = value
    self.value_type = value_type
    self.line = line
    self.col = col