'''
Configy confguration container
'''
# pylint: disable=W0212,R0903
import os
from copy import deepcopy
import yaml


class xdict(dict):

    def __init__(self, *a, **kw):
        super(xdict, self).__init__(*a, **kw)

    def __getitem__(self, item):
        val = super(xdict, self).__getitem__(item)
        if isinstance(val, dict):
            return xdict(val)
        return val

    def __getattr__(self, item):
        return self[item]


class ConfigContainer(object):
    '''
    Singleton containing configuration
    '''

    def __init__(self):
        self._config = xdict()

    def _set_config(self, conf):
        self._config = xdict(conf)

    def _get_config(self):
        return self._config

    def __getitem__(self, item):
        '''
        Override .get() to use config reference correctly
        '''
        return self._config[item]

    def __getattr__(self, attr):
        '''
        Override getattr() so config.SOME_VALUE works transparently
        '''
        return self._config[attr]

config = ConfigContainer()

def extend_config(conf, data):
    for k, v in data.items():
        if isinstance(v, dict) and isinstance(conf.get(k, None), dict):
            conf[k] = extend_config(conf[k], v)
        else:
            conf[k] = v
    return conf

def load_file(name):
    '''
    Loads the given file by name as a dict object.
    Returns None on error.
    '''
    if name:
        try:
            with open(name) as fil:
                val = yaml.load(fil)
            if isinstance(val, dict):
                return val
        except (IOError, yaml.error.YAMLError):
            pass
    return None

def build_config(conf=None, env=None, defaults=None, data=None):

    # 1) data
    if isinstance(data, dict):
        val = deepcopy(data)
    else:
        val = {}

    # 2) defaults
    _val = load_file(defaults)
    if _val:
        val = extend_config(val, _val)

    # 3) conf/env
    if env:
        _conf = os.environ.get(env, conf)
        _val = load_file(_conf)
        if not _val:
            env=None
    if not env:
        _val = load_file(conf)
    if _val:
        val = extend_config(val, _val)

    return val

def load_config(conf=None, env=None, defaults=None, data=None):
    config._set_config(build_config(conf, env, defaults, data))

