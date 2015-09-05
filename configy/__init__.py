'''
Simple Configuration manager, plays well with testing
'''

__all__ = ['config', 'load_config', 'testconfig']
__version__ = '0.1.0'

from . import testconfig
from .config_container import config, load_config

