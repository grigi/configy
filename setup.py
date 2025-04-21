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

setup(
    name='configy',
    version=get_version('configy/__init__.py'),
    description='Simple Configuration manager, plays well with testing',
    long_description=open('README.rst').read(),
    author='Nickolas Grigoriadis',
    author_email='nagrigoriadis@gmail.com',
    url='https://github.com/grigi/configy',
    zip_safe=False,

    # Dependencies
    install_requires=[
        'PyYAML',
    ],

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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

