'''
Simple Configuration manager, plays well with testing
'''
from .config_container import ConfigyError, config, load_config
from .helpers import to_bool

__version__ = '0.1.4'
__all__ = ('config', 'load_config', 'ConfigyError', 'to_bool')
