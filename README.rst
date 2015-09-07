#######
configy
#######

Simple Configuration manager, plays well with testing.

.. image:: https://travis-ci.org/grigi/configy.svg
    :target: https://travis-ci.org/grigi/configy?branch=master
.. image:: https://coveralls.io/repos/grigi/configy/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/grigi/configy?branch=master

Basic Usage
===========

Specify the configuration directives as early in execution as possible:

.. code-block:: python

    import configy
    
    # Every option is optional, fill in as makes sense.
    configy.load_config(
        conf='the_configuration.yaml',  # The default config file if not specified as an ENV var
        env='CONFIGY_FILE',             # The ENV var to look for a config file
        defaults='defaults.yaml',       # The defaults that is always loaded.
        data={'manual': 'defaults'}     # Manually provided defaults loaded
    )

Given a sample YAML config file of:

.. code-block:: YAML

    Something:
      value: The Value

You then use it so:

.. code-block:: python

    >>> from configy import config
    >>> config.Something.value
    'The Value'

If you try to access any configuration value that isn't defined you will get an exception:

.. code-block:: python

    >>> config.Something.other
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 'other'

The config object is just a dictionary, so you can use it as a regular dictionary as well:

.. code-block:: python

    >>> config['Something']['value']
    'The Value'
    >>> config.Something.get('other', 'default value')
    'default value'


How to overload settings for testing
====================================

During testing, one often wants to override some configuration to test something specific.
Configy supports this use case.

.. code-block:: python

    from configy import config, testconfig
    
    @testconfig.override_config({
        'Something': {
            'other': 'I now exist',
        },
        'Extra': 'defined',
    })
    def test_override():
        assert config.Something.other == 'I now exist'
        assert config.Extra == 'defined'

One can also define configuration to be used:

.. code-block:: python

    @testconfig.load_config(
        conf='test_config.yaml'
    )
    def test_load_config():
        assert config.testvalue == 'test result'

You can also define the WHOLE configuration that is loaded for that test:

.. code-block:: python

    @testconfig.load_config(data={
        'testvalue': 'test result',
    })
    def test_load_config_data():
        assert config.testvalue == 'test result'

All the testing decorators will work on method, class and function level.
