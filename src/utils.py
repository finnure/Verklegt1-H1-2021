import string

SPECIAL_CHARACTERS = 'ÁáÐðÉéÍíÓóÚúÝýÞþÆæÖö'
PRINTABLE = string.printable
ALL_PRINTABLE = PRINTABLE + SPECIAL_CHARACTERS
NUMBERS = '0123456789'
PHONE = '+0123456789'


def none_if_not_list(list) -> 'list | None':
  ''' Returns list if it is a list, else returns None '''
  return list if type(list) is list else None

########### Validation #################

def validate_headers(required_headers: 'list[str]', headers: 'list[str]') -> None:
  ''' Checks if all required headers are present. Throws an error if they're not. '''
  for header in required_headers:
    if header not in headers:
      raise KeyError(f'validate_headers() missing header {header}')

def validate_phone(value: str) -> None:
  ''' Checks if phone number is valid. Raises error if it's not. '''
  for idx, digit in enumerate(value):
    if not digit.isdigit():
      if idx > 0 or digit != '+':
        raise ValueError(f'{value} is not a valid phone number.')

def validate_email(email: str) -> None:
  ''' TODO '''

