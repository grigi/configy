'''
Configy confguration container
'''
# pylint: disable=W0212,R0903
import os
import re
from copy import deepcopy
from typing import Any

import yaml


class ConfigyError(Exception):
    '''
    Configy exception handler
    '''


env_pattern = re.compile(r".*?\${(.*?)}.*?")
def env_constructor(loader, node):  # type: ignore
    '''
    Adds ENVVAR syntax support
    '''
    value = loader.construct_scalar(node)
    for group in env_pattern.findall(value):
        envvar = os.environ.get(group)
        if envvar is None:
            raise ConfigyError(f"Environment variable '{group}' is not defined!")
        value = value.replace("${%s}" % group, envvar)
    return value

yaml.add_implicit_resolver("!pathex", env_pattern)
yaml.add_constructor("!pathex", env_constructor)


class CDict(dict):
    '''
    Dict-type that allows accessing by attribute
    '''

    def __init__(self, *a: Any, **kw: Any) -> None:
        super().__init__(*a, **kw)

    def __getitem__(self, item: str) -> Any:
        val = super().__getitem__(item)
        if isinstance(val, dict):
            return CDict(val)
        return val

    def __getattr__(self, item: str) -> Any:
        return self[item]


class ICDict(CDict):
    '''
    Case-insensitive dict-type that allows accessing by attribute
    '''

    def __getitem__(self, item: str) -> Any:
        val = super().__getitem__(item.lower())
        if isinstance(val, dict):
            return ICDict(val)
        return val


class ConfigContainer:
    '''
    Singleton containing configuration
    '''

    def __init__(self) -> None:
        self._config = CDict()
        self._case_sensitive = True

    def _set_config(self, conf: dict, case_sensitive: bool|None=None) -> None:
        '''
        Private helper to set the config data to new dict
        '''
        if case_sensitive is None:
            case_sensitive = self._case_sensitive
        else:
            self._case_sensitive = case_sensitive

        if case_sensitive:
            self._config = CDict(conf)
        else:
            self._config = ICDict(conf)

    def _get_config(self) -> CDict:
        '''
        Private helper that gets the actual config data
        '''
        return self._config

    def __getitem__(self, item: str) -> Any:
        '''
        Override .get() to use config reference correctly
        '''
        return self._config[item]

    def __getattr__(self, attr: str) -> Any:
        '''
        Override getattr() so config.SOME_VALUE works transparently
        '''
        return self._config[attr]

    def __iter__(self):
        '''
        Makes base config iterable
        '''
        return self._config.__iter__()

    def keys(self):
        '''
        Makes base config mappable
        '''
        return self._config.keys()

config = ConfigContainer()  # pylint: disable=C0103


def extend_config(conf: dict, data: dict) -> dict:
    '''
    Extends the config by replacing the overwriting the dataset granularily.
    '''
    for key, val in data.items():
        if isinstance(val, dict) and isinstance(conf.get(key, None), dict):
            conf[key] = extend_config(conf[key], val)
        else:
            conf[key] = val
    return conf


def load_file(name: str) -> dict|None:
    '''
    Loads the given file by name as a dict object.
    Returns None on error.
    '''
    if name:
        try:
            with open(name, encoding="utf-8") as fil:
                val = yaml.load(fil, Loader=yaml.FullLoader)
            if isinstance(val, dict):
                return val
            if val is None:
                pass
            else:
                raise ConfigyError(f"File '{name}' does not contain key-value pairs")
        except OSError as exc:
            raise ConfigyError(f"File '{name}' does not exist") from exc
        except yaml.error.YAMLError as exc:
            raise ConfigyError(f"File '{name}' is not a valid YAML document") from exc
    return None


def build_config(conf=None, env=None, defaults=None, data=None, case_sensitive=True):
    '''
    Builds the config for load_config. See load_config for details.
    '''

    # 1) data
    res = deepcopy(data) if isinstance(data, dict) else {}

    # 2) defaults
    _res = load_file(defaults)
    if _res:
        res = extend_config(res, _res)

    # 3) conf/env
    if env:
        conf = os.environ.get(env, conf)
    _res = load_file(conf)
    if _res:
        res = extend_config(res, _res)

    if not case_sensitive:
        def recursive_lowkey(dic):
            '''Recursively lowercases dict keys'''
            _dic = {}
            for key, val in dic.items():
                if isinstance(val, dict):
                    val = recursive_lowkey(val)
                _dic[key.lower()] = val
            return _dic
        res = recursive_lowkey(res)

    return res


def load_config(conf=None, env=None, defaults=None, data=None, case_sensitive=True):
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

    case_sensitive
        Defaults to True, set to False if you want case insensitive config
    '''
    config._set_config(build_config(conf, env, defaults, data), case_sensitive)
