class FileHandler():
  ''' Each data class creates an instance of file handler. '''

  def __init__(self, filename: str, data_folder: str, headers: list):
    self.filename = filename
    if data_folder != '' and not data_folder.endswith('/'):
      # If data_folder is not empty it needs to end with a forward slash
      data_folder += '/'
    self.data_folder = data_folder
    self.headers = headers
    try:
      self.open('r')
    except FileNotFoundError:
      self.open('w')
      self.write()
    self.close()


  def open(self, mode, encoding = 'utf-8'):
    ''' Opens file using mode and optional encoding and places the handle on self '''
    self.__file_handle = open(self.data_folder + self.filename, mode, encoding=encoding)

  def close(self):
    ''' Closes the file handle if it's open '''
    if not self.__file_handle.closed:
      self.__file_handle.close()

  def read(self):
    ''' Reads data from file and returns as list '''
    pass

  def write(self, data = None):
    ''' Writes data to file '''
    pass

  def update(self):
    ''' Updates a line in the file '''
    pass
