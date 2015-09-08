'''
Contains helper tools for handling configuration
'''

def to_bool(val, default=False):
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

