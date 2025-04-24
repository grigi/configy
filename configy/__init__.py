'''
Simple Configuration manager, plays well with testing
'''
from .config_container import ConfigyError, config, load_config
from .helpers import to_bool

__version__ = '0.1.4'
__all__ = ('ConfigyError', 'config', 'load_config', 'to_bool')
