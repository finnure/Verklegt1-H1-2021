from typing import Type
from ui.form import Form
from dlapi import DlApi
from models.location import Location

class LocationLogic():

  def __init__(self, dlapi: Type[DlApi]) -> None:
    self.dlapi = dlapi

  def new(self, form: Form) -> Location:
    ''' TODO '''
    loc = self.__parse_form(form)
    location = self.dlapi.add_location(loc)
    return self.add_extras(location)

  def update(self, form: Form) -> Location:
    ''' TODO '''
    loc = self.__parse_form(form)
    location= self.dlapi.update_location(loc.id, loc)
    return self.add_extras(location)

  def get(self, id: int) -> Location:
    ''' TODO '''
    location = self.dlapi.get_one_location(id)
    if location is None:
      return
    return self.add_extras(location)

  def get_all(self) -> 'list[Location]':
    ''' TODO '''
    locations = self.dlapi.get_all_locations()
    return [self.add_extras(loc) for loc in locations]

  def add_extras(self, location: Location):
    filter = {'location_id': location.id}
    buildings = self.dlapi.get_filtered_buildings(filter)
    manager = self.dlapi.get_one_employee(location.manager_id)
    employees = self.dlapi.get_filtered_employees(filter)
    contractors = self.dlapi.get_filtered_contractors(filter)
    location.set_buildings(buildings)
    location.set_manager(manager)
    location.set_employees(employees)
    location.set_contractors(contractors)
    return location


  def __parse_form(self, form: Form) -> Location:
    ''' Returns instance of Location if everything is ok. '''
    try:
      id = form['id']
    except StopIteration:
      id = 0

    return Location(
        id, 
        form['country'],
        form['city'],
        form['airport'],
        form['address'],
        form['phone'],
        form['opening_hours'],
        form['manager']
      )