from dlapi import DlApi
from models.accessory import Accessory
from ui.form import Form
from utils import Helpers

class AccessoryLogic():

  def __init__(self, dlapi: DlApi) -> None:
    self.dlapi = dlapi

  def new(self, form: Form, building_id: int):
    acc = self.__parse_form(form, building_id)
    accessory = self.dlapi.add_accessory(acc)
    return self.add_extras(accessory)

  def update(self, form: Form):
    acc = self.__parse_form(form)
    accessory = self.dlapi.update_accessory(acc.id, acc)
    return self.add_extras(accessory)

  def get(self, id: int):
    accessory = self.dlapi.get_one_accessory(id)
    if accessory is None:
      return
    return self.add_extras(accessory)

  def get_all(self):
    accessories = self.dlapi.get_all_accessories()
    return [self.add_extras(acc) for acc in accessories]

  def get_filtered(self, filter):
    accessories = self.dlapi.get_filtered_accessories(filter)
    return [self.add_extras(acc) for acc in accessories]

  def update_maintenance(self, accessory: Accessory):
    accessory.update_maintained(Helpers.get_current_date())
    acc = self.dlapi.update_accessory(accessory.id, accessory)
    return self.add_extras(acc)

  def add_extras(self, accessory: Accessory):
    building = self.dlapi.get_one_building(accessory.building_id)
    accessory.set_building(building)
    return accessory

  def __parse_form(self, form: Form, building_id: int = None) -> Accessory:
    ''' Returns instance of Accessory if everything is ok. '''
    try:
      id = form['id']
    except StopIteration:
      id = 0
    if building_id is None:
      building_id = form['building_id']
    return Accessory(
        id, 
        building_id,
        form['name'],
        form['description'],
        form['state'],
        form['bought'],
        form['last_maintained'],
      )
