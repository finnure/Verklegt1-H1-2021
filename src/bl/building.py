from dlapi import DlApi
from models.building import Building
from ui.form import Form

class BuildingLogic():

  def __init__(self, dlapi: DlApi) -> None:
    self.dlapi = dlapi

  def new(self, form: Form, location_id: int):
    building = self.__parse_form(form, location_id)
    return self.dlapi.add_building(building)

  def update(self, form: Form):
    building = self.__parse_form(form)
    return self.dlapi.update_building(building.id, building)

  def get(self, id: int):
    return self.dlapi.get_one_building(id)

  def get_all(self):
    return self.dlapi.get_all_buildings()

  def get_filtered(self, filter):
    return self.dlapi.get_filtered_buildings(filter)

  def __parse_form(self, form: Form, location_id: int = None) -> Building:
    ''' Returns instance of Building if everything is ok. '''
    try:
      id = form['id']
    except StopIteration:
      id = 0
    if location_id is None:
      location_id = form['location_id']
    return Building(
        id, 
        form['registration'],
        location_id,
        form['description'],
        form['state'],
        form['address'],
        form['size'],
        form['rooms'],
        form['type'],
      )
