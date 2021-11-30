from llapi import LlApi
from ui.screen import Screen
class LoginView():

  def __init__(self, screen: Screen, llapi: LlApi):
    self.__screen = screen
    self.llapi = llapi

  def display_view(self):
    self.__screen.print('ENTER USER ID:', 2, 6)

  def invalid_input_error(self):
    self.__screen.print('Invalid input, user id should be a number. Please try again', 4, 6)

  def user_not_found_error(self):
    self.__screen.print('No user found, please try again!', 4, 6)

  def get_input(self):
    while True:
      # user_id = self.__screen.get_string(2, 21, 3, '0123456789')
      user_id = self.__screen.get_string(2, 21)
      self.__screen.delete_line(4)
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
      
