
from pypack import data

class NestedMessage(data.msg):
    a = data.str
    b = data.float
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __eq__(self, obj):
        return self.a == obj.a and self.b == obj.b


class TestMessage(data.msg):
    a = data.str
    b = data.int
    c = data.float
    d = data.list(data.int)
    e = data.dict(data.str, data.float)
    f = data.list(NestedMessage)
    g = NestedMessage

    def __init__(self, a, b, c, d, e, f, g):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g


def test():
    # create some object
    m = TestMessage('Hi!', 10, 3.14, [4, 5], {'one': 0.999, 'two': 2.0001}, [NestedMessage('foo', 2.71), NestedMessage('bar', -1)], NestedMessage('baz', 8))

    # serialize it
    data = m.pack()
    print data
    print m.pypack_members
    print type(NestedMessage)
    assert data == ('Hi!', 10, 3.14, (4, 5), {'one': 0.999, 'two': 2.0001}, (('foo', 2.71), ('bar', -1)), ('baz', 8))

    # unserialize it
    m2 = TestMessage.load(data)


    # it's the same!
    assert m.a == m2.a
    assert m.b == m2.b
    assert m.c == m2.c
    assert m.d == m2.d
    assert m.e == m2.e
    assert m.f == m2.f
    assert m.g == m2.g
