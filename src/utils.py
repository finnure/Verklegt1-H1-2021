import string
from typing import Callable

SPECIAL_CHARACTERS = 'ÁáÐðÉéÍíÓóÚúÝýÞþÆæÖö'
PRINTABLE = string.printable
ALL_PRINTABLE = PRINTABLE + SPECIAL_CHARACTERS
NUMBERS = '0123456789'
PHONE = '+0123456789'


def none_if_not_list(list) -> 'list | None':
  ''' Returns list if it is a list, else returns None '''
  return list if type(list) is list else None

########### Validators #################

def validate_headers(required_headers: 'list[str]', headers: 'list[str]') -> None:
  ''' Checks if all required headers are present. Throws an error if they're not. '''
  for header in required_headers:
    if header not in headers:
      raise KeyError(f'validate_headers() missing header {header}')


def validate_min_length(min_length: int) -> 'Callable[[str],None]':
  ''' Raises an error if value is not long enough.
  Must call first with min length and then again with value.
  Example: `validate_min_length(5)(value)` raises an error if 
  value length is less than 5. '''
  def apply_validation(value) -> None:
    if len(value) < min_length:
      raise ValueError(f'MINIMUM LENGTH OF {min_length} REQUIRED')
  return apply_validation

def validate_options(options: 'list | dict') -> 'Callable[[str], None]':
  ''' Raises an error if value is not in options list or key in options dict.
  Must call first with options list or dict and then again with value.
  Example: `validate_options([val1, val2, val3])(value)` raises an
  error if value is not equal to one of val1, val2 or val3. '''
  def apply_validation(value) -> None:
    if value not in options:
      raise ValueError(f'INVALID OPTION {value}')
  return apply_validation

def validate_phone(value: str) -> None:
  ''' Raises error if phonenumber is not valid. '''
  if value[0] not in PHONE or not value[1:].isnumeric():
    raise ValueError(f'{value} IS NOT A VALID PHONE NUMBER')

def validate_email(email: str) -> None:
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
  

def validate_ssn(ssn: str) -> None:
  ''' TODO '''