
import structpack


def test_version():
    assert structpack.version == '1.3.0'

'''
A trivial example that shows how to use Structpack
'''
class Point(structpack.msg):
    x = structpack.float
    y = structpack.float
    z = structpack.float

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def test_point():
    p1 = Point(1., 2., 3.)
    json = p1.pack()
    assert json == (1., 2., 3.)
    p2 = Point.load(json)
    assert p1.x == p2.x
    assert p1.y == p2.y
    assert p1.z == p2.z


def test_point_names():
    p1 = Point(1., 2., 3.)
    json = p1.pack(with_names=True)
    assert json == {'x': 1., 'y': 2., 'z': 3.}
    p2 = Point.load(json, True)
    assert p1.x == p2.x
    assert p1.y == p2.y
    assert p1.z == p2.z



'''
Structpack can serialize nested objects with the `child` field, if those objects themselves
are serializable.
'''
class Circle(structpack.msg):
    center = structpack.child(Point)
    radius = structpack.float

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius


def test_circle():
    c1 = Circle(Point(1., 2., 3.), 4.)
    json = c1.pack()
    assert json == ((1., 2., 3.), 4.)
    c2 = Circle.load(json)
    assert c1.center.x == c2.center.x
    assert c1.center.y == c2.center.y
    assert c1.center.z == c2.center.z
    assert c1.radius == c2.radius


def test_circle_names():
    c1 = Circle(Point(1., 2., 3.), 4.)
    json = c1.pack(True)
    assert json == {'center': {'x': 1., 'y': 2., 'z': 3.}, 'radius': 4.}
    c2 = Circle.load(json)
    assert c1.center.x == c2.center.x
    assert c1.center.y == c2.center.y
    assert c1.center.z == c2.center.z
    assert c1.radius == c2.radius



class NestedMessage(structpack.msg):
    a = structpack.str
    b = structpack.float
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __eq__(self, obj):
        return self.a == obj.a and self.b == obj.b


class TestMessage(structpack.msg):
    a = structpack.str
    b = structpack.int
    c = structpack.float
    d = structpack.list(structpack.int)
    e = structpack.dict(structpack.str, structpack.float)
    f = structpack.list(NestedMessage)
    g = structpack.child(NestedMessage)

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
    json = m.pack()
    print json
    print type(NestedMessage)
    assert json == ('Hi!', 10, 3.14, (4, 5), {'one': 0.999, 'two': 2.0001}, (('foo', 2.71), ('bar', -1)), ('baz', 8))

    # unserialize it
    m2 = TestMessage.load(json)


    # it's the same!
    assert m.a == m2.a
    assert m.b == m2.b
    assert m.c == m2.c
    assert m.d == m2.d
    assert m.e == m2.e
    assert m.f == m2.f
    assert m.g == m2.g

'''
Structpack will include all fields from inherited classes when packing a derived class
'''
def test_inheritance():
    class Foo(structpack.msg):
        a = structpack.int
    class Bar(Foo):
        b = structpack.int
    b = Bar()
    b.a = 1
    b.b = 2

    data = b.pack()
    assert data == (1, 2)

    b2 = b.load(data)
    assert b2.a == 1
    assert b2.b == 2


'''
Derived classes can override the inherited fields also
'''
def test_inheritance_override():
    class Foo(structpack.msg):
        a = structpack.int
    class Bar(Foo):
        a = structpack.str
    b = Bar()
    b.a = 'hi'
    data = b.pack()
    assert data == ('hi',)

    b2 = b.load(data)
    assert b2.a == 'hi'


def test_list():
    class Foo(structpack.msg):
        a = structpack.int
        def __init__(self, a):
            self.a = a
    class Bar(structpack.msg):
        items = structpack.list(Foo)
    b = Bar()
    b.items = [Foo(1), Foo(2)]
    data = b.pack()
    assert data == (((1,), (2,)),)
    b2 = b.load(data)
    assert b2.items[0].a == 1
    assert b2.items[1].a == 2


'''
Structpack will try to convert object attributes to the correct type defined in the class before packing them
'''
def test_types():
    class Foo(structpack.msg):
        a_int = structpack.int
        a_float = structpack.float

    f = Foo()
    f.a_int = 3.14
    f.a_float = 2
    data = f.pack()
    assert data == (3, 2.0)

'''
Structpack can also pass through arbitrary native object with the `value` type
'''
def test_value():
    class Foo(structpack.msg):
        x = structpack.value

    f = Foo()
    f.x = [1]
    data = f.pack()
    assert data == ([1,],)
    f2 = f.load(data)
    assert f2.x == f.x


'''
Structpack can use default values defined in the class fields if no attribute is set on the object
TODO: implement this
'''
def _test_default():
    class Foo(structpack.msg):
        a = structpack.int(defualt=0)

    f = Foo()
    data = f.pack()
    assert data == (0,)

