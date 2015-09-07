'''
Configy confguration container
'''
# pylint: disable=W0212,R0903
import os
from copy import deepcopy
import yaml


class ConfigyError(Exception):
    '''
    Configy exception handler
    '''
    pass


class CDict(dict):
    '''
    Dict-type that allows accessing by attribute
    '''

    def __init__(self, *a, **kw):
        super(CDict, self).__init__(*a, **kw)

    def __getitem__(self, item):
        val = super(CDict, self).__getitem__(item)
        if isinstance(val, dict):
            return CDict(val)
        return val

    def __getattr__(self, item):
        return self[item]


class ConfigContainer(object):
    '''
    Singleton containing configuration
    '''

    def __init__(self):
        self._config = CDict()

    def _set_config(self, conf):
        '''
        Private helper to set the config data to new dict
        '''
        self._config = CDict(conf)

    def _get_config(self):
        '''
        Private helper that gets the actual config data
        '''
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

config = ConfigContainer()  # pylint: disable=C0103


def extend_config(conf, data):
    '''
    Extends the config by replacing the overwriting the dataset granularily.
    '''
    for key, val in data.items():
        if isinstance(val, dict) and isinstance(conf.get(key, None), dict):
            conf[key] = extend_config(conf[key], val)
        else:
            conf[key] = val
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
            elif val is None:
                pass
            else:
                raise ConfigyError(
                    "File '%s' does not contain key-value pairs" % name)
        except IOError:
            raise ConfigyError("File '%s' does not exist" % name)
        except yaml.error.YAMLError:
            raise ConfigyError("File '%s' is not a valid YAML document" % name)
    return None


def build_config(conf=None, env=None, defaults=None, data=None):
    '''
    Builds the config for load_config. See load_config for details.
    '''

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
        conf = os.environ.get(env, conf)
    _val = load_file(conf)
    if _val:
        val = extend_config(val, _val)

    return val


def load_config(conf=None, env=None, defaults=None, data=None):
    '''
    Loads configuration and sets the config singleton.

    In order of least precedence:
    data
        Manually provided defaults as dict
    defaults
        File-name of defaults to load
    env
        Overrides conf file-name based on existance of env var with this name.
        If env-var points to non-existing or unparseable file, then conf is
         loaded as per usual.
    conf
        Default configuration file if ``env`` doesn't exist.
    '''
    config._set_config(build_config(conf, env, defaults, data))
