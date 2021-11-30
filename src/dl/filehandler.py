import csv

class FileHandler():
  ''' Each data class creates an instance of file handler. 
  It needs to pass in filename, data_folder and headers list.
  Headers list is a list of strings containing all column names. '''

  def __init__(self, filename: str, data_folder: str, headers: list):
    self.filename = filename
    if data_folder != '' and not data_folder.endswith('/'):
      # If data_folder is not empty it needs to end with a forward slash
      data_folder += '/'
    self.data_folder = data_folder
    self.headers = headers

  def read(self):
    ''' Reads data from file and returns as list of dicts '''
    with open(self.data_folder + self.filename, 'r', newline='', encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      return [row for row in reader]

  def write(self, data: list):
    ''' Writes data to file. File will be overwritten so data needs to contain all lines.
    Any lines that are left out will be lost forever! '''
    with open(self.data_folder + self.filename, 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=self.headers)
      writer.writeheader()
      writer.writerows(data)

  def add(self, data: dict):
    ''' Adds one line to end of file '''
    with open(self.data_folder + self.filename, 'a', newline='', encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=self.headers)
      writer.writerow(data)
