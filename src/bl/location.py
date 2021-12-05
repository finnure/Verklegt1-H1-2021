from typing import Type
from ui.form import Form
from dlapi import DlApi
from models.location import Location

class LocationLogic():

  def __init__(self, dlapi: Type[DlApi]) -> None:
    self.dlapi = dlapi
    self.required_headers = [
      'country',
      'city',
      'airport',
      'address',
      'phone',
      'openinghours',
      'manager'
    ]

  def new(self, form: Form) -> Location:
    ''' TODO '''
    loc = self.__parse_form(form)
    return self.dlapi.add_location(loc)

  def update(self, form: Form) -> Location:
    ''' TODO '''
    loc = self.__parse_form(form)
    return self.dlapi.update_location(loc.id, loc)

  def get(self, id: int) -> Location:
    ''' TODO '''
    return self.dlapi.get_one_location(id)

  def get_all(self):
    ''' TODO '''
    return self.dlapi.get_all_locations()

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
        form['openinghours'],
        form['manager']
      )