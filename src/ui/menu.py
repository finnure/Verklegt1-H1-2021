class Menu():

  def __init__(self, line: int = 3, col: int = 5, spacing: int = 4):
    self.start_line = line
    self.start_col = col
    self.spacing = spacing
    self.menu_items: 'list[MenuItem]' = []

  def add_menu_item(self, option: str, name: str, connection) -> None:
    ''' Adds a new menu item to the menu.
    Name is what is displayed after the menu option.
    Option is the character that selects this menu item.
    Connection is the ui object that should be called when this item is selected
    line and col mark the spot where form field should appear.'''
    self.menu_items.append(MenuItem(option, name, connection))

  def get_options(self) -> 'dict[str,str]':
    ''' Returns all options from menu items as a dict 
    containing option as key and connection as value. '''
    return {item.option: item.connection for item in self.menu_items}

  def __getitem__(self, index):
    ''' Make menu subscriptable. Menu items can be accessed using menu[idx] '''
    if isinstance(index, slice):
      return self.menu_items[index.start:index.stop:index.step]
    return self.menu_items[index]

  def __iter__(self):
    ''' Make menu iterable, can be used in a for loop with: for item in menu '''
    return iter(self.menu_items)

class MenuItem():
  def __init__(self, option: str, name: str, connection:str = None):
    self.name = name
    self.option = option
    self.connection = connection

  def __str__(self):
    return f'{self.option} = {self.name} for {self.connection}'
