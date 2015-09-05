'''
configy test suite
'''
import configy

try:
    import unittest2 as unittest #pylint: disable=F0401
except ImportError:
    import unittest

class ConfigyTest(unittest.TestCase):
    '''
    Tests configy regular behaviour
    '''

    def setUp(self):
        pass

    def test_empty_config(self):
        pass

