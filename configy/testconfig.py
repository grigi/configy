from functools import wraps
from copy import deepcopy
from .config_container import *

import json

def override_config(data):
    def wrap(callback):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            old_config = config._get_config()
            new_config = extend_config(json.loads(json.dumps(old_config)), data)
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
    def wrap(callback):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            old_config = config._get_config()
            config._set_config(build_config(**kwconf))
            try:
                ret = callback(*args, **kwargs)
            except:
                config._set_config(old_config)
                raise 
            config._set_config(old_config)
            return ret
        return wrapper
    return wrap

