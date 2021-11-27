from typing import Union

def none_if_not_list(list) -> Union[list,None]:
  ''' Returns list if it is a list, else returns None '''
  return list if type(list) is list else None