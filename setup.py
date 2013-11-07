import structpack
from setuptools import setup

setup(
    name        = 'structpack',
    version     = structpack.__version__,
    url         = 'https://github.com/Knio/structpack',
    author      = 'Tom Flanagan',
    author_email= 'tom@zkpq.ca',
    description = '''A Python library for serializing and deserializing object trees to JSON-compatable values (dicts, lists, strings, ints, floats, bools).''',
    long_description = open('README.md').read(),
    license = 'MIT',
    packages=['structpack'],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
