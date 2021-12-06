from dlapi import DlApi
from models.contractor import Contractor
from ui.form import Form

class ContractorLogic():

  def __init__(self, dlapi: DlApi) -> None:
    self.dlapi = dlapi

  def new(self, form: Form, location_id: int):
    contractor = self.__parse_form(form, location_id)
    return self.dlapi.add_contractor(contractor)

  def update(self, form: Form):
    contractor = self.__parse_form(form)
    return self.dlapi.update_contractor(contractor)

  def get(self, id: int):
    return self.dlapi.get_one_contractor(id)

  def get_all(self):
    return self.dlapi.get_all_contractors()

  def get_filtered(self, filter):
    return self.dlapi.get_filtered_contractors(filter)

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
