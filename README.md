structpack
==========

A Python library for serializing and deserializing object trees to JSON-compatable values (dicts, lists, strings, ints, floats, bools).

[![Build Status](https://travis-ci.org/Knio/structpack.svg?branch=master)](https://travis-ci.org/Knio/structpack)
[![Coverage Status](https://coveralls.io/repos/Knio/structpack/badge.png)](https://coveralls.io/r/Knio/structpack)


Installation
------------

The recommended way to install structpack is with [pip](http://pypi.python.org/pypi/pip/):

    pip install structpack

[![PyPI version](https://badge.fury.io/py/structpack.png)](http://badge.fury.io/py/structpack)


Examples
========

`structpack` is designed to be a base class (`msg`) that you inherit from and add properties to (`bool`, `int`, `float`, `string`, `list`, and `dict`).

The `msg` class adds methods `pack` and `load` which convert your object to and from native types, respectively.

The following is a trivial example of how to make a `Point` type using structpack

    import structpack
    class Point(structpack.msg):
        x = structpack.float
        y = structpack.float
        z = structpack.float
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    >>> p1 = Point(1., 2., 3.)
    >>> data = p1.pack()
    >>> print data
    (1.0, 2.0, 3.0)

    >>> p2 = Point.load(data)
    >>> print p2
    <__main__.Point object at 0x0000000001EDA390>
    >>> print p2.x, p2.y, p2.z
    1.0 2.0 3.0


More
----

Please see the [test suite](https://github.com/Knio/structpack/blob/master/tests/test_structpack.py) for more examples until they are documented here.


TODO
====

- Docs / examples
- Type check values
- Benchmark & optimize
