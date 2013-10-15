pypack
======

A Python library for serializing and deserializing objects to JSON-compatable
values. `pypack` preserves the *data* and the *structure* of your objects,
but not the type or field names, so it's a nice compact represtation of your
data if you know how to reconstruct it, but should not be used when the data
format is not well defined.
