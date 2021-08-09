'''
Simple Configuration manager, plays well with testing
'''
from . import testconfig
from .config_container import config, load_config, ConfigyError
from .helpers import to_bool

__version__ = '0.1.2'
