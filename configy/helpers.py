'''
Contains helper tools for handling configuration
'''
from typing import Optional


def to_bool(val: Optional[str], default: Optional[bool]=None) -> Optional[bool]:
    '''
    Converts string to bool

    True
        'y', 'yes', '1', 't','true'
    False
        'n', 'no', '0', 'f', 'false'
    else
        defaults to default (False, by default)
    '''
    val = str(val).lower()
    if val in ['y', 'yes', '1', 't', 'true']:
        return True
    if val in ['n', 'no', '0', 'f', 'false']:
        return False
    return default
