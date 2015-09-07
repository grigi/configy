'''
configy test suite
'''
import os
from configy import config, testconfig, load_config

BASE_DIR = os.path.dirname(__file__)

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

# Set some Env Variable
os.environ['CONFIGY_FILE'] = os.path.join(BASE_DIR, 'testdata/conf3.yaml')
os.environ['CONFIGY_NOTFILE'] = os.path.join(BASE_DIR, 'testdata/notconf.yaml')

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

    @testconfig.load_config(
        conf=os.path.join(BASE_DIR, 'testdata/conf1.yaml')
    )
    def test_config_conf(self):
        with self.assertRaises(KeyError):
            config.Something.one

        self.assertEqual(config.conf1, 'value')
        self.assertEqual(config.baseconf.one, 'value')

    @testconfig.load_config(
        conf=os.path.join(BASE_DIR, 'testdata/conf2.yaml'),
        defaults=os.path.join(BASE_DIR, 'testdata/conf1.yaml')
    )
    def test_config_conf_default(self):
        with self.assertRaises(KeyError):
            config.Something.one
        
        self.assertEqual(config.conf1, 'value')
        self.assertEqual(config.conf2, 'value2')
        self.assertEqual(config.baseconf.one, 'value2')
        self.assertEqual(config.baseconf.two, 'value2')

    @testconfig.load_config(
        conf=os.path.join(BASE_DIR, 'testdata/conf2.yaml'),
        env='CONFIGY_FILE',
        defaults=os.path.join(BASE_DIR, 'testdata/conf1.yaml')
    )
    def test_config_conf_env(self):
        with self.assertRaises(KeyError):
            config.Something.one
        with self.assertRaises(KeyError):
            config.conf2

        self.assertEqual(config.conf1, 'value')
        self.assertEqual(config.conf3, 'value3')
        self.assertEqual(config.baseconf.one, 'value')
        self.assertEqual(config.baseconf.three, 'value3')

    @testconfig.load_config(
        conf=os.path.join(BASE_DIR, 'testdata/conf2.yaml'),
        env='CONFIGY_NOTEXIST',
        defaults=os.path.join(BASE_DIR, 'testdata/conf1.yaml')
    )
    def test_config_conf_undef_env(self):
        with self.assertRaises(KeyError):
            config.Something.one

        self.assertEqual(config.conf1, 'value')
        self.assertEqual(config.conf2, 'value2')
        self.assertEqual(config.baseconf.one, 'value2')
        self.assertEqual(config.baseconf.two, 'value2')

    @testconfig.load_config(
        conf=os.path.join(BASE_DIR, 'testdata/conf2.yaml'),
        env='CONFIGY_NOTFILE',
        defaults=os.path.join(BASE_DIR, 'testdata/conf1.yaml')
    )
    def test_config_conf_bad_env(self):
        with self.assertRaises(KeyError):
            config.Something.one

        self.assertEqual(config.conf1, 'value')
        self.assertEqual(config.conf2, 'value2')
        self.assertEqual(config.baseconf.one, 'value2')
        self.assertEqual(config.baseconf.two, 'value2')


