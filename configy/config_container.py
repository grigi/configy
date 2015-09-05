'''
Configy confguration container
'''
# pylint: disable=W0212,R0903

class xdict(dict):

    __deepcopy__ = None

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
    def recursive_update(_conf, _data):
        for k, v in _data.items():
            if isinstance(v, dict) and isinstance(_conf[k], dict):
                _conf[k] = recursive_update(_conf[k], v)
            else:
                _conf[k] = v
        return _conf

    return recursive_update(conf, data)

def build_config(conf=None, env=None, defaults=None, data=None):
    return data

def load_config(conf=None, env=None, defaults=None, data=None):
    config._set_config(build_config(conf, env, defaults, data))

