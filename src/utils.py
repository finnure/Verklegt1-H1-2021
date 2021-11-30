import string

SPECIAL_CHARACTERS = 'ÁáÐðÉéÍíÓóÚúÝýÞþÆæÖö'
SPECIAL_CHARACTERS_ASCII = [
  129, # Á
  161, # á
  144, # Ð
  176, # ð
  137, # É
  169, # é
  141, # Í
  173, # í
  147, # Ó
  179, # ó
  154, # Ú
  186, # ú
  157, # Ý
  189, # ý
  158, # Þ
  190, # þ
  134, # Æ
  166, # æ
  150, # Ö
  182, # ö
]
PRINTABLE = string.printable
ALL_PRINTABLE = PRINTABLE + SPECIAL_CHARACTERS
NUMBERS = '0123456789'


def none_if_not_list(list) -> 'list | None':
  ''' Returns list if it is a list, else returns None '''
  return list if type(list) is list else None

def convert_ascii_to_str(prop: 'list | int') -> str:
  ''' Converts prop to ascii character.
  If prop is a list, a string is returned.
  If prop is an int, a string character is returned '''
  if type(prop) is int:
    return chr(prop)
  elif type(prop) is list:
    str_list = []
    for item in prop:
      if type(item) is int:
        str_list.append(str(item))
      else:
        raise TypeError(f'convert_ascii_to_str() expected list item to be of type int, got {item} of type {type(item)}')
    return ''.join(str_list)
  else:
    raise TypeError(f'convert_ascii_to_str() expected list or int, got {prop} of type {type(prop)}')

def get_ascii_list(prop: 'list | str') -> list:
  ''' Detects if prop is a string or list.
  If it's a list, it converts each item to it's ascii value if needed.
  If it's a string, it converts it to a list of ascii values.
  For each character, both upper and lowercase are added. '''
  if type(prop) is str:
    upper_list = [ord(char.upper()) for char in prop]
    lower_list = [ord(char.lower()) for char in prop]
    if SPECIAL_CHARACTERS in prop:
      # Fix because Icelandic characters suck!!
      upper_list.extend(SPECIAL_CHARACTERS_ASCII)
    # Join upper and lower lists, add them to a set to remove duplicates and change back to list
    return list(set(upper_list + lower_list))
  elif type(prop) is list:
    upper_list = [validate_ascii_list(item) for item in prop]
    lower_list = [chr(item).lower() for item in upper_list]
    # Join upper and lower lists, add them to a set to remove duplicates and change back to list
    return list(set(upper_list + lower_list))
  else:
    raise TypeError(f'get_ascii_list() expected list or str, got {prop} of type {type(prop)}')
    

def validate_ascii_list(prop: 'str | int') -> int:
  ''' Converts prop to ascii value if it isn't already.
  Type str must be of length 1. It is converted to uppercase.
  If type int is of length 1 it is converted to string and ascii value returned.
  If type int is of length > 1, it is returned as ascii number of uppercase value '''
  if type(prop) is str:
    return ord(prop.upper())
  elif type(prop) is int:
    if len(str(prop)) == 1:
      return ord(str(prop))
    else:
      return ord(chr(prop).upper())
  else:
    raise TypeError(f'validate_ascii_list() expected int or str, got {prop} of type {type(prop)}')


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

