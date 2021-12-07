from dl.filehandler import FileHandler
from models.report import ContractorReport

class ContractorReportData():

  def __init__(self, data_folder):
    self.headers = [
      'id',
      'report_date',
      'contractor_id',
      'employee_report_id',
      'description',
      'approved',
      'note',
      'hours',
      'contractor_fee',
      'contractor_rating'
    ]
    self.data_folder = data_folder
    self.__file = FileHandler('contractor_reports.csv', self.data_folder, self.headers)

  def add(self, contractorreport: ContractorReport) -> ContractorReport:
    ''' Add ContractorReport to file. Gets next available id from csv file and 
    adds it to dict before adding to file. Returns contractorreport if successful. '''
    con_rep = contractorreport.as_dict()
    con_rep['id'] = self.__get_next_id()
    self.__file.add(con_rep)
    return self.__parse(con_rep)

  def update(self, id: int, contractorreport: ContractorReport) -> ContractorReport:
    ''' Updates contractor reports. Gets all data from file, replaces contractor report
    that matches id and writes all data back to file. '''
    contractorreports = self.get_all()
    # Ternary with list comprehension. This replaces contractor report in list if con_rep.id matches id
    updated_contractorreport = [contractorreport.as_dict() if con_rep.id == id else con_rep.as_dict() for con_rep in contractorreports]
    self.__file.write(updated_contractorreport)
    return self.get_one(id)

  def delete(self, id: int) -> None:
    ''' Removes contractor report from file. Gets all data from file, filters contractor report
    that matches id from the list and writes all data back to file '''
    contractorreports = self.get_all()
    filtered_contractorreports = [con_rep.as_dict() for con_rep in contractorreports if con_rep.id != id]
    self.__file.write(filtered_contractorreports)

  def get_all(self) -> 'list[ContractorReport]':
    ''' Get all contractor reports from file and return as list of ContractorReport instances. '''
    contractor_reports = self.__file.read()
    return [self.__parse(con_rep) for con_rep in contractor_reports]

  def get_one(self, id: int) -> 'ContractorReport | None':
    ''' Find contractor report matching the id specified. If no contractor_report is found, None is returned '''
    contractor_reports = self.get_all()
    for contractor_report in contractor_reports:
      if contractor_report.id == id:
        return contractor_report

  def get_filtered(self, filter: dict, partial_match: bool = False) -> 'list[ContractorReport]':
    ''' Get a list of ContractorsReports matching filter specified.
    Filter should be a dict where key is the Contractor field to be matched and 
    value the value you're searching for. If filter includes more than one key, all keys
    need to match. If partial_match is true we do a partial match. Default is full match. '''
    contractor_reports = self.get_all()
    for key, val in filter.items():
      if key in self.headers:
        if partial_match:
          filtered_contractor_reports = [con_rep for con_rep in contractor_reports if str(val).lower() in str(getattr(con_rep, key)).lower()]
        else:
          filtered_contractor_reports = [con_rep for con_rep in contractor_reports if str(val).lower() == str(getattr(con_rep, key)).lower()]
      else:
        # Wrong key in filter. Raise error
        raise KeyError(f'Invalid filter key for ContractorReport: {key}')
    return filtered_contractor_reports

  def __parse(self, contractor_report: 'dict[str,str]') -> ContractorReport:
    ''' Converts data to either a dict or an instance of ContractorReport '''
    return ContractorReport(
      int(contractor_report['id']), 
      int(contractor_report['contractor_id']),
      int(contractor_report['employee_report_id']),
      contractor_report['description'],
      contractor_report['approved'],
      contractor_report['note'],
      float(contractor_report['hours']),
      int(contractor_report['contractor_fee']),
      float(contractor_report['contractor_rating']),
    )


  def __get_next_id(self) -> int:
    ''' Finds max id and returns id+1 '''
    contractorreport = self.get_all()
    all_ids = [con_rep.id for con_rep in contractorreport]
    return max(all_ids) + 1