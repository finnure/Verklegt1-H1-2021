class Menu():

  def __init__(self):
    self.menu_items = []

  def add_menu_item(self, name: str, option: str, connection, line: int, col: int) -> None:
    ''' Adds a new menu item to the menu.
    Name is what is displayed after the menu option.
    Option is the character that selects this menu item.
    Connection is the ui object that should be called when this item is selected
    line and col mark the spot where form field should appear.'''
    self.menu_items.append(MenuItem(name, option, connection, line, col))

  def get_options(self):
    ''' Returns all options from menu items as a list '''
    return [item.option for item in self.menu_items]

  def __getitem__(self, index):
    ''' Make menu subscriptable. Menu items can be accessed using menu[idx] '''
    if isinstance(index, slice):
      return self.menu_items[index.start:index.stop:index.step]
    return self.menu_items[index]

  def __iter__(self):
    ''' Make menu iterable, can be used in a for loop with: for item in menu '''
    return iter(self.menu_items)

class MenuItem():
  def __init__(self, name: str, option: str, connection, line: int, col: int):
    self.name = name
    self.option = option
    self.connection = connection
    self.line = line
    self.col = col

  def __str__(self):
    return f'{self.option} = {self.name} at {self.col}x{self.line}'
