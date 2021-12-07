class Table():

  def __init__(self, data, headers: 'dict[str,str]', begin_line: int = 5, begin_col: int = 6, max_lines: int = 20, numerate: bool = True) -> None:
    self.data = data
    self.headers = headers
    self.begin_line = begin_line
    self.begin_col = begin_col
    self.max_lines = max_lines
    self.numerate = numerate
    self.__add_columns()
    self.__pages_info()

  def __pages_info(self):
    if len(self.columns) > 0:
      self.pages = self.columns[0].pages
      self.current_page = self.columns[0].current_page

  def next_page(self) -> None:
    [col.next_page() for col in self.columns]
    self.__pages_info()

  def previous_page(self) -> None:
    [col.previous_page() for col in self.columns]
    self.__pages_info()

  def first_page(self) -> None:
    [col.first_page() for col in self.columns]
    self.__pages_info()

  def last_page(self) -> None:
    [col.last_page() for col in self.columns]
    self.__pages_info()


  def __add_columns(self) -> None:
    self.columns: 'list[TableColumn]' = []
    if self.numerate:
      self.columns.append(TableColumn('#', list(range(1, len(self.data) + 1)), self.max_lines))
    for key, name in self.headers.items():
      rows = [getattr(item, key) for item in self.data]
      self.columns.append(TableColumn(name.upper(), rows, self.max_lines))

  def __getitem__(self, index):
    ''' Make table subscriptable. Table items can be accessed using table[idx]. '''
    if isinstance(index, slice):
      return self.columns[index.start:index.stop:index.step]
    return self.columns[index]

  def __iter__(self):
    ''' Make table iterable, can be used in a for loop with: for column in table. '''
    return iter(self.columns)

class TableColumn():

  def __init__(self, name: str, rows: 'list[str | int]', max_lines: int) -> None:
    self.name = name
    self.rows = rows
    self.max_lines = max_lines
    self.pages = len(rows) // max_lines
    self.current_page = 0

    
  def get_width(self) -> int:
    ''' Returns length of longest word in rows + 4. '''
    return max([len(str(row)) for row in self.rows] + [len(self.name)]) + 4

  def __getitem__(self, index):
    ''' Make column subscriptable. Column row can be accessed using column[idx]. '''
    if isinstance(index, slice):
      return self.rows[index.start:index.stop:index.step]
    return self.rows[index]

  def __iter__(self):
    ''' Make column iterable, can be used in a for loop with: for row in column.
    If rows are more than max lines, paging will be applied. '''
    if self.pages > 0:
      curr = self.current_page
      next = curr + 1
      rows = self.max_lines
      return iter(self.rows[curr * rows:next * rows])
    else:
      return iter(self.rows)

  def next_page(self):
    if self.current_page < self.pages:
      self.current_page += 1
    return self.current_page
  
  def last_page(self):
    self.current_page = self.pages
    return self.current_page

  def previous_page(self):
    if self.current_page > 0:
      self.current_page -= 1
    return self.current_page

  def first_page(self):
    self.current_page = 0
    return self.current_page