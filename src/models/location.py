class Location():

  def __init__(self, id: int, country: str, airport: str, phone: int, openinghours: str) -> None:
    self.id = id
    self.country = country
    self.airport = airport
    self.phone = phone
    self.openinghours = openinghours
    self.employees = []
    self.buildings = []
    self.contractors = []

  def __str__(self) -> str:
    pass

