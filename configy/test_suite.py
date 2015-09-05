'''
configy test suite
'''
from configy import config, testconfig, load_config

try:
    import unittest2 as unittest #pylint: disable=F0401
except ImportError:
    import unittest

# Load some default config
load_config(data={
    'Something': {
        'one': '1',
    },
})

class ConfigyTest(unittest.TestCase):
    '''
    Tests configy regular behaviour
    '''

    def test_config_not_exist(self):
        with self.assertRaises(KeyError):
            config.moo

    def test_config_string(self):
        self.assertEqual(config.Something.one, '1')

    @unittest.skip('not implemented')
    def test_config_casting_int(self):
        val = config.Something.one.as_int()
        self.assertNotEqual(val, '1')
        self.assertEqual(val, 1)

    @unittest.skip('not implemented')
    def test_config_casting_bool(self):
        val = config.Something.one.as_bool()
        self.assertTrue(val)

    @testconfig.override_config({
        'Something': {
            'two': '2',
        },
        'Extra': 'definition',
    })
    def test_config_override(self):
        self.assertEqual(config.Something.one, '1')
        self.assertEqual(config.Something.two, '2')
        self.assertEqual(config.Extra, 'definition')

    @testconfig.load_config(data={
        'Nothing': 'new',
    })
    def test_config_load_config_override(self):
        with self.assertRaises(KeyError):
            config.Something.one

        self.assertEqual(config.Nothing, 'new')


