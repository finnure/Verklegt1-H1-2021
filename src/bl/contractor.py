from dlapi import DlApi
from models.contractor import Contractor
from ui.form import Form

class ContractorLogic():

  def __init__(self, dlapi: DlApi) -> None:
    self.dlapi = dlapi

  def new(self, form: Form, location_id: int):
    contractor = self.__parse_form(form, location_id)
    con = self.dlapi.add_contractor(contractor)
    return self.add_extras(con)

  def update(self, form: Form):
    contractor = self.__parse_form(form)
    con = self.dlapi.update_contractor(contractor)
    return self.add_extras(con)

  def get(self, id: int):
    con = self.dlapi.get_one_contractor(id)
    if con is None:
      return
    return self.add_extras(con)

  def get_all(self):
    contractors = self.dlapi.get_all_contractors()
    return [self.add_extras(con) for con in contractors]

  def get_filtered(self, filter):
    contractors = self.dlapi.get_filtered_contractors(filter)
    return [self.add_extras(con) for con in contractors]

  def add_extras(self, contractor: Contractor):
    filter = {'contractor_id': contractor.id}
    location = self.dlapi.get_one_location(contractor.location_id)
    reports = self.dlapi.get_filtered_contractor_reports(filter)
    contractor.set_location(location)
    contractor.set_reports(reports)
    return contractor

  def __parse_form(self, form: Form, location_id: int = None) -> Contractor:
    ''' Returns instance of Building if everything is ok. '''
    try:
      id = form['id']
    except StopIteration:
      id = 0
    if location_id is None:
      location_id = form['location_id']
    return Contractor(
        id, 
        location_id,
        form['name'],
        form['contact'],
        form['phone'],
        form['openinghours'],
        form['email'],
        form['speciality'],
      )
