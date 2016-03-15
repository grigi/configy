'''
configy test suite
'''
# pylint: disable=W0104
import os
from configy import config, testconfig, load_config, ConfigyError, to_bool
from configy.config_container import build_config

BASE_DIR = os.path.dirname(__file__)

try:
    import unittest2 as unittest  # pylint: disable=F0401
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

    def test_config_attribute_not_exist(self):
        '''Config attribute fails with KeyError when it doesn't exist.'''
        with self.assertRaises(KeyError):
            config.moo

    def test_config_item_not_exist(self):
        '''Config item fails with KeyError when it doesn't exist'''
        with self.assertRaises(KeyError):
            config['moo']

    def test_config_attribute(self):
        '''Config attribute traversal works'''
        self.assertEqual(config.Something.one, '1')

    def test_config_item(self):
        '''Config item traversal works'''
        self.assertEqual(config['Something']['one'], '1')

    @testconfig.override_config({
        'Something': {
            'two': '2',
        },
        'Extra': 'definition',
    })
    def test_config_override(self):
        '''override_config extends the config'''
        self.assertEqual(config.Something.one, '1')
        self.assertEqual(config.Something.two, '2')
        self.assertEqual(config.Extra, 'definition')

    @testconfig.load_config(data={
        'Nothing': 'new',
    })
    def test_load_config_override(self):
        '''load_config replaces the config'''
        with self.assertRaises(KeyError):
            config.Something.one

        self.assertEqual(config.Nothing, 'new')

    @testconfig.load_config(
        conf=os.path.join(BASE_DIR, 'testdata/conf1.yaml')
    )
    def test_load_config_conf(self):
        '''load_config: conf file loads'''
        with self.assertRaises(KeyError):
            config.Something.one

        self.assertEqual(config.conf1, 'value')
        self.assertEqual(config.baseconf.one, 'value')

    @testconfig.load_config(
        conf=os.path.join(BASE_DIR, 'testdata/conf2.yaml'),
        defaults=os.path.join(BASE_DIR, 'testdata/conf1.yaml')
    )
    def test_load_config_conf_defaults(self):
        '''load_config: conf extends defaults file granularily'''
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
    def test_load_config_conf_env(self):
        '''load_config: env overrides conf'''
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
    def test_load_config_conf_undef_env(self):
        '''load_config: graecfully ignores non-set ENV val'''
        with self.assertRaises(KeyError):
            config.Something.one

        self.assertEqual(config.conf1, 'value')
        self.assertEqual(config.conf2, 'value2')
        self.assertEqual(config.baseconf.one, 'value2')
        self.assertEqual(config.baseconf.two, 'value2')

    def test_load_config_conf_bad_env(self):
        '''load_config: raises ConfigyError for non-existing file'''
        with self.assertRaises(ConfigyError):
            build_config(
                conf=os.path.join(BASE_DIR, 'testdata/conf2.yaml'),
                env='CONFIGY_NOTFILE',
                defaults=os.path.join(BASE_DIR, 'testdata/conf1.yaml')
            )

    def test_build_config_not_parseable(self):
        '''build_config: raises ConfigyError for non-parseable file'''
        with self.assertRaises(ConfigyError):
            build_config(
                conf=os.path.join(BASE_DIR, 'testdata/notparseable'),
                defaults=os.path.join(BASE_DIR, 'testdata/conf1.yaml')
            )

    def test_build_config_conf_empty(self):
        '''build_config: ignores empty document'''
        val = build_config(
            conf=os.path.join(BASE_DIR, 'testdata/empty'),
            defaults=os.path.join(BASE_DIR, 'testdata/conf1.yaml')
        )
        self.assertEqual(val, {'conf1': 'value', 'baseconf': {'one': 'value'}})

    def test_build_config_conf_not_dict(self):
        '''build_config: raises ConfigyError for keyed config files'''
        with self.assertRaises(ConfigyError):
            build_config(
                conf=os.path.join(BASE_DIR, 'testdata/list.yaml'),
                defaults=os.path.join(BASE_DIR, 'testdata/conf1.yaml')
            )

    def test_override_config_fail(self):
        '''override_config: Restores config after function exception'''
        @testconfig.override_config(data={'Something': {'one': '2'}})
        def override_fail():
            '''raises Exception'''
            raise Exception('Failing on purpose')

        self.assertEqual(config.Something.one, '1')
        with self.assertRaisesRegexp(Exception, 'Failing on purpose'):
            override_fail()
        self.assertEqual(config.Something.one, '1')

    def test_load_config_fail(self):
        '''load_config: Restores config after function exception'''
        @testconfig.load_config(data={})
        def load_fail():
            '''raises Exception'''
            raise Exception('Failing on purpose')

        self.assertEqual(config.Something.one, '1')
        with self.assertRaisesRegexp(Exception, 'Failing on purpose'):
            load_fail()
        self.assertEqual(config.Something.one, '1')

    @testconfig.load_config(
        data={
            'Something': {
                'one': '1',
            },
        },
        case_sensitive=False
    )
    def test_case_insensitivity(self):
        '''Case insensitive mode'''
        self.assertEqual(config.someThinG.ONE, '1')
        self.assertEqual(config.Something.one, '1')
        self.assertEqual(config.sOMETHING.ONE, '1')

    @testconfig.load_config(data={
        'value': 'The Value',
        'number': '42',
        'bool1': '1',
        'bool2': 'FALSE',
        'bool3': 'y',
    })
    def test_to_bool(self):
        '''to_bool'''
        self.assertTrue(to_bool(config.bool1))
        self.assertFalse(to_bool(config.bool2))
        self.assertTrue(to_bool(config.bool3))
        self.assertFalse(to_bool(config.number))
        self.assertFalse(to_bool(config.value))
        self.assertIsNone(to_bool(config.number, None))
        self.assertTrue(to_bool(config.bool3, None))

    @testconfig.load_config(data={'a': 1, 'b': 2})
    def test_dict(self):
        '''dict(config) should work'''
        self.assertEqual(dict(config), {'a': 1, 'b': 2})

    @testconfig.load_config(data={'a': 1, 'b': 2})
    def test_keys(self):
        '''config.keys() should work'''
        self.assertEqual(sorted(list(config.keys())), ['a', 'b'])

    @testconfig.load_config(data={'a': 1, 'b': 2})
    def test_list(self):
        '''list(config) should work'''
        self.assertEqual(sorted(list(config)), ['a', 'b'])

    @testconfig.load_config(data={'a': 1, 'b': 2})
    def test_iter(self):
        '''iter(config) should work'''
        self.assertEqual(sorted(list(iter(config))), ['a', 'b'])

