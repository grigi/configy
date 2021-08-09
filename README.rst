#######
configy
#######

Simple Configuration manager, plays well with testing.

.. image:: https://travis-ci.com/grigi/configy.svg?branch=master
    :target: https://travis-ci.com/grigi/configy
.. image:: https://coveralls.io/repos/grigi/configy/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/grigi/configy?branch=master


Basic Usage
===========

Install from pypi:

.. code-block:: shell

    pip install configy

Specify the configuration directives as early in execution as possible:

.. code-block:: python

    import configy
    
    try:
        # Every option is optional, fill in as makes sense.
        configy.load_config(
            conf='the_configuration.yaml',  # The default config file if not specified as an ENV var
            env='CONFIGY_FILE',             # The ENV var to look for a config file
            defaults='defaults.yaml',       # The defaults that is always loaded.
            data={'manual': 'defaults'},    # Manually provided defaults loaded
            case_sensitive=True             # Case Sensitive by default
        )
    except configy.ConfigyError as e:
        # Report config load error to user
    
Given a sample YAML config file of:

.. code-block:: YAML

    Something:
      value: The Value
      number: 42
      bool1: 1
      bool2: FALSE
      bool3: y

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


Helper functions
----------------

Since you can't guarantee the type of a value in the configuration files (YAML treats everything as text), you need to do type conversion manually.

For ints and floats it is easy:

.. code-block:: python

    >>> int(config.Something.number)
    42
    >> float(config.Something.number)
    42.0

For booleans it is a bit more tricky, as a boolean can be represented by many different notations. You also don't have complete control over the notation used. For this we provide a ``to_bool()`` helper function.

It treats case-insensitively 

``True``
    'y', 'yes', '1', 't','true'
``False``
    'n', 'no', '0', 'f', 'false'

Anything else will resort to the provided default (which defaults to False)

.. code-block:: python

    >>> from configy import config, to_bool
    >>> to_bool(config.Something.bool1)
    True
    >>> to_bool(config.Something.bool2)
    False
    >>> to_bool(config.Something.bool1)
    True
    >>> to_bool(config.Something.number)
    False
    >>> to_bool(config.Something.number, True)
    True
    >>> to_bool(config.Something.number, None)
    None


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
        # Existing values still work as per usual
        assert config.Something.value == 'The Value'
        # New values 
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
