import sys
from setuptools import setup, find_packages

def get_version(fname):
    import re
    verstrline = open(fname, "rt").read()
    mo = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", verstrline, re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (fname,))

def get_test_requirements():
    requirements = []
    if sys.version_info[0:2] == (2, 6):
        requirements.append('unittest2')
    return requirements

setup(
    name='configy',
    version=get_version('configy/__init__.py'),
    description='Simple Configuration manager, plays well with testing',
    long_description=open('README.rst').read(),
    author='Nickolas Grigoriadis',
    author_email='nagrigoriadis@gmail.com',
    url='https://github.com/grigi/configy',
    zip_safe=False,
    test_suite='configy.test_suite',

    # Dependencies
    install_requires=[
        'PyYAML',
    ],
    tests_require=get_test_requirements(),

    # Packages
    packages=find_packages(),
    include_package_data=True,

    # Scripts
    scripts=[],

    # Classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

