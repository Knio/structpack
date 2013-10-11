
from pypack import data

class TestMessage(data.msg):
    a = data.str
    b = data.int
    c = data.float

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


def test():
    # create some object
    m = TestMessage('Hi!', 10, 3.14)

    # serialize it
    data = m.pack()

    # unserialize it
    m2 = TestMessage.load(data)


    # it's the same!
    assert m.a == m2.a
    assert m.b == m2.b
    assert m.c == m2.c
