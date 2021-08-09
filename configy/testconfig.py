'''
Configy test helper functions
'''
# pylint: disable=W0212,W0142
from functools import wraps
from configy.config_container import config, build_config, extend_config

import json


def override_config(data):
    '''
    Overrides a partial configuration set for the test function/method
    '''
    def wrap(callback):  # pylint: disable=C0111
        @wraps(callback)
        def wrapper(*args, **kwargs):  # pylint: disable=C0111
            old_config = config._get_config()
            new_config = extend_config(
                json.loads(json.dumps(old_config)),
                data
            )
            config._set_config(new_config)
            try:
                ret = callback(*args, **kwargs)
            except:
                config._set_config(old_config)
                raise
            config._set_config(old_config)
            return ret
        return wrapper
    return wrap


def load_config(**kwconf):
    '''
    Replaces the whole configuration set for the test function/method
    '''
    def wrap(callback):  # pylint: disable=C0111
        @wraps(callback)
        def wrapper(*args, **kwargs):  # pylint: disable=C0111
            old_config = config._get_config()
            case_sensitive = kwconf.get('case_sensitive', True)
            old_case_sensitive = config._case_sensitive
            config._set_config(build_config(**kwconf), case_sensitive)
            try:
                ret = callback(*args, **kwargs)
            except:
                config._set_config(old_config, old_case_sensitive)
                raise
            config._set_config(old_config, old_case_sensitive)
            return ret
        return wrapper
    return wrap
