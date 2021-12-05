from llapi import LlApi
from ui.screen import Screen
class LoginView():

  def __init__(self, screen: Screen, llapi: LlApi):
    self.__screen = screen
    self.llapi = llapi

  def display_view(self):
    self.__screen.clear()
    self.__screen.print('ENTER USER ID:', 2, 6)
    self.__screen.print('Q TO QUIT', 3, 6)

  def invalid_input_error(self):
    self.display_view()
    self.__screen.print('Invalid input, user id should be a number. Please try again', 5, 6, 'ERROR')

  def user_not_found_error(self):
    self.display_view()
    self.__screen.print('User not found, please try again!', 5, 6, 'ERROR')

  def get_input(self):
    self.display_view()
    while True:
      user_id = self.__screen.get_string(2, 21, 3, 'Qq0123456789')
      if 'Q' in user_id.upper():
        return
      try:
        id = int(user_id)
      except ValueError:
        self.invalid_input_error()
        continue
      user = self.llapi.get_employee(id)
      if user is not None:
        return user
      else:
        self.user_not_found_error()
      
