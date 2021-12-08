from dlapi import DlApi
from models.building import Building
from ui.form import Form

class BuildingLogic():

  def __init__(self, dlapi: DlApi) -> None:
    self.dlapi = dlapi

  def new(self, form: Form, location_id: int):
    building = self.__parse_form(form, location_id)
    build =  self.dlapi.add_building(building)
    return self.add_extras(build)

  def update(self, form: Form):
    building = self.__parse_form(form)
    build =  self.dlapi.update_building(building.id, building)
    return self.add_extras(build)

  def get(self, id: int):
    building =  self.dlapi.get_one_building(id)
    return self.add_extras(building)

  def get_all(self):
    buildings = self.dlapi.get_all_buildings()
    return [self.add_extras(build) for build in buildings]

  def get_filtered(self, filter):
    buildings = self.dlapi.get_filtered_buildings(filter)
    return [self.add_extras(build) for build in buildings]

  def get_buildings_by_location(self, location_id):
    filter = {'location_id': location_id}
    return self.get_filtered(filter)

  def add_extras(self, building: Building) -> Building:
    filter = {'building_id': building.id}
    location = self.dlapi.get_one_location(building.location_id)
    accessories = self.dlapi.get_filtered_accessories(filter)
    tasks = self.dlapi.get_filtered_tasks(filter)
    building.set_location(location)
    building.set_accessories(accessories)
    building.set_tasks(tasks)
    return building    

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
