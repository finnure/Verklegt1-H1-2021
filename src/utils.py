import string
from typing import Callable
from datetime import datetime

class Filters():
  ''' String constants used in filters. '''
  SPECIAL_CHARACTERS = 'ÁáÐðÉéÍíÓóÚúÝýÞþÆæÖö'
  PRINTABLE = string.printable
  ALL_PRINTABLE = PRINTABLE + SPECIAL_CHARACTERS
  NUMBERS = '0123456789'
  FLOATS = '.0123456789'
  PHONE = '+0123456789 '
  USER_ID = 'Qq0123456789'
  DATE = '-0123456789'

def none_if_not_list(list) -> 'list | None':
  ''' Returns list if it is a list, else returns None '''
  return list if type(list) is list else None

class Helpers():
  ''' Helper functions. '''

  @staticmethod
  def get_multiline_string(text: str, cols: int) -> 'list[str]':
    ''' Splits a string into multiple lines, each of cols length. '''
    start_i = 0
    lines = []
    while True:
      if len(text[start_i:]) <= cols:
        lines.append(text[start_i:])
        break
      next_i = text.rindex(' ', start_i, start_i + cols)
      lines.append(text[start_i:next_i])
      start_i = next_i + 1
    return lines

  @staticmethod
  def get_current_date():
    date, _ = str(datetime.now()).split()
    return date

  @staticmethod
  def date_between(start, end, value) -> bool:
    ''' Checks if date value is between start date and end date.
    Returns True if it is, False otherwise. '''
    return datetime.fromisoformat(start) < datetime.fromisoformat(value) < datetime.fromisoformat(end)

  @staticmethod
  def is_date(check, value) -> bool:
    ''' Checks if date value matches check date. '''
    return datetime.fromisoformat(check) == datetime.fromisoformat(value)


########### Validators #################
class Validate():
  ''' Input validation methods. '''
  
  @staticmethod
  def headers(required_headers: 'list[str]', headers: 'list[str]') -> None:
    ''' Checks if all required headers are present. Throws an error if they're not. '''
    for header in required_headers:
      if header not in headers:
        raise KeyError(f'validate_headers() missing header {header}')

  @staticmethod
  def min_length(min_length: int) -> 'Callable[[str],None]':
    ''' Raises an error if value is not long enough.
    Must call first with min length and then again with value.
    Example: `validate_min_length(5)(value)` raises an error if 
    value length is less than 5. '''
    def apply_validation(value) -> None:
      if len(value) < min_length:
        raise ValueError(f'MINIMUM LENGTH OF {min_length} REQUIRED')
    return apply_validation

  @staticmethod
  def required(value) -> None:
    ''' Raises an error if value is an empty string. '''
    if value == '':
      raise ValueError('THIS FIELD IS REQUIRED')

  @staticmethod
  def options(options: 'list | dict') -> 'Callable[[str], None]':
    ''' Raises an error if value is not in options list or key in options dict.
    Must call first with options list or dict and then again with value.
    Example: `validate_options([val1, val2, val3])(value)` raises an
    error if value is not equal to one of val1, val2 or val3. '''
    def apply_validation(value) -> None:
      if value not in options:
        raise ValueError(f'INVALID OPTION {value}')
    return apply_validation

  @staticmethod
  def phone(value: str) -> None:
    ''' Raises error if phonenumber is not valid. '''
    if value[0] not in Filters.PHONE or not value[1:].isnumeric():
      raise ValueError(f'{value} IS NOT A VALID PHONE NUMBER')

  @staticmethod
  def email(email: str) -> None:
    ''' Raises an error if email is not valid '''
    for c in email:
      if c in string.whitespace:
        raise ValueError('WHITESPACE NOT ALLOWED IN EMAIL')
      if c in string.punctuation and c not in '.@-_':
        raise ValueError(f'ILLEGAL CHARACTER {c} IN EMAIL')
    if '@' not in email:
      raise ValueError('@ MISSING FROM EMAIL')
    if len([c for c in email if c == '@']) > 1:
      raise ValueError('ONLY ONE @ ALLOWED IN EMAIL')
    user, domain = email.split('@')
    if len(domain) == 0 or len(user) == 0:
      raise ValueError('EMAIL CAN NOT START OR END WITH @')
    if '.' not in domain:
      raise ValueError('DOMAIN PART MUST INCLUDE A DOT')
    if not user[0].isalnum():
      raise ValueError('EMAIL MUST START WITH A NUMBER OR CHARACTER')
    domain_parts = domain.split('.')
    if len(domain_parts[-1]) < 2:
      raise ValueError('TLD OF DOMAIN MUST BE AT LEAST 2 CHARACTERS')
    
  @staticmethod
  def ssn(ssn: str) -> None:
    ''' TODO '''

  @staticmethod
  def date(date: str) -> None:
    '''Raises an error if date format is incorrect'''
    if date is None or date == '':
      return
    year,month,day = date.split('-')
    if len(year) != 4:
      raise ValueError('YEAR MUST BE 4 DIGITS')
    if len(month) != 2: 
      raise ValueError('MONTH MUST BE 2 DIGITS')
    if len(day) != 2: 
      raise ValueError('DAY MUST BE 2 DIGITS')
    if int(month) < 1 or int(month) > 12: 
      raise ValueError(f'INVALID VALUE FOR MONTH {month}')
    if int(day) < 1 or int(day) > 31:
      raise ValueError(f'INVALID VALUE FOR DAY {day}')


  @staticmethod
  def float_num(value: str) -> None:
    '''Raise error if more than one . is in value'''
    if len([c for c in value if c == '.']) > 1:
      raise ValueError('ONLY ONE DOT ALLOWED IN VALUE')
