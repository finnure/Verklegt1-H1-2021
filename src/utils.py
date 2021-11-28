from typing import Union
import string

PRINTABLE_IS = 'ÁáÐðÉéÍíÓóÚúÝýÞþÆæÖö'
PRINTABLE = string.printable
ALL_PRINTABLE = PRINTABLE + PRINTABLE_IS
NUMBERS = '0123456789'


def none_if_not_list(list) -> Union[list,None]:
  ''' Returns list if it is a list, else returns None '''
  return list if type(list) is list else None

def convert_ascii_to_str(prop: Union[list, int]) -> str:
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
        raise ValueError(f'Expected list item to be of type int, got {item} of type {type(item)}')
    return ''.join(str_list)
  else:
    raise ValueError(f'Expected list or int, got {prop} of type {type(prop)}')

def get_ascii_list(prop: Union[list, str]) -> list:
  ''' Detects if prop is a string or list.
  If it's a list, it converts each item to it's ascii value if needed.
  If it's a string, it converts it to a list of ascii values.
  For each character, both upper and lowercase are added. '''
  if type(prop) is str:
    upper_list = [ord(char.upper()) for char in prop]
    lower_list = [ord(char.lower()) for char in prop]
    # Join upper and lower lists, add them to a set to remove duplicates and change back to list
    return list(set(upper_list + lower_list))
  elif type(prop) is list:
    upper_list = [validate_ascii_list(item) for item in prop]
    lower_list = [chr(item).lower() for item in upper_list]
    # Join upper and lower lists, add them to a set to remove duplicates and change back to list
    return list(set(upper_list + lower_list))
  else:
    raise ValueError(f'Expected list or str, got {prop} of type {type(prop)}')
    

def validate_ascii_list(prop: Union[str, int]) -> int:
  ''' Converts prop to ascii value if it isn't already.
  Type str must be of length 1. It is converted to uppercase.
  If type int is of length 1 it is converted to string and ascii value returned.
  If type int is of length > 1, it is returned as ascii number of uppercase value '''
  if type(prop) is str and len(prop) == 1:
    return ord(prop.upper())
  elif type(prop) is int:
    if len(str(prop)) == 1:
      return ord(str(prop))
    else:
      return ord(chr(prop).upper())
  else:
    raise ValueError(f'Expected int or str of length 1, got {prop} of type {type(prop)}')
