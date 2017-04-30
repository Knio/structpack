
class PackType(object):
    __id = 0
    def __init__(self):
        PackType.__id += 1
        self.id = PackType.__id

    def __lt__(self, other):
        return self.id < other.id


class PrimitiveType(PackType):
    native = None
    @classmethod
    def load(cls, a, **kwargs):
        return a

    @classmethod
    def pack(cls, a, **kwargs):
        return cls.native(a)


class Value(PrimitiveType):
    @classmethod
    def pack(cls, a, **kwargs):
        return a

class Bool(PrimitiveType):
    native = bool

class Int(PrimitiveType):
    native = int

class Float(PrimitiveType):
    native = float

class Str(PrimitiveType):
    native = str

class Bytes(PrimitiveType):
    native = bytes


class Struct():
    pass


class StructMember(PackType):
    def __init__(self, fmt):
        super(StructMember, self).__init__()
        self.fmt = fmt

STRUCT_TYPES = [
    ('x', 'padbyte'),
    ('c', 'char'),
    ('b', 'signedchar'),
    ('B', 'unsignedchar'),
    ('_', 'bool'),
    ('h', 'short'),
    ('H', 'unsignedshort'),
    ('i', 'int'),
    ('I', 'unsignedint'),
    ('l', 'long'),
    ('L', 'unsignedlong'),
    ('q', 'longlong'),
    ('Q', 'unsignedlonglong'),
    ('n', 'ssize_t'),
    ('N', 'size_t'),
    ('e', 'halffloat'),
    ('f', 'float'),
    ('d', 'double'),
    ('s', 'bytes'),
    ('p', 'pascal'),
    ('P', 'void'),
]

for fmt, name in STRUCT_TYPES:
    @property
    def _func(self):
        return StructMember(fmt)
    setattr(Struct, name, _func)

struct = Struct()

class List(PackType):
    def __init__(self, cls):
        PackType.__init__(self)
        self.cls = cls

    def load(self, a, **kwargs):
        return list(self.cls.load(i, **kwargs) for i in a)

    def pack(self, a, **kwargs):
        return tuple(self.cls.pack(i, **kwargs) for i in a)


class Dict(PackType):
    def __init__(self, keycls, valcls):
        PackType.__init__(self)
        self.keycls = keycls
        self.valcls = valcls

    def load(self, a, **kwargs):
        return {self.keycls.load(k, **kwargs): self.valcls.load(v, **kwargs)
            for k, v in a.items()}

    def pack(self, a, **kwargs):
        return {self.keycls.pack(k, **kwargs): self.valcls.pack(v, **kwargs)
            for k, v in a.items()}


class Reference(PackType):
    def __init__(self, cls):
        PackType.__init__(self)
        self.cls = cls
        self.load = cls.load
        self.pack = cls.pack


class MessageMeta(type):
    def __init__(cls, name, bases, dict):
        super(MessageMeta, cls).__init__(name, bases, dict)
        # collect attributes
        members = {}
        for c in reversed(cls.__mro__):
            for v in getattr(c, '_struct_members', []):
                members[v.name] = v
        for k, v in dict.items():
            if isinstance(v, PackType):
                v.name = k
                members[k] = v
        cls._struct_members = sorted(members.values())


MessageBase = MessageMeta('MessageBase', (object,), {})
class Message(MessageBase):
    def __init__(self, *args, **kwargs):
        if args and kwargs:
            raise ValueError('default constructor only accepts positional \
                arguments or keyword arguments, not both')
        if args:
            self.replace(args)
        if kwargs:
            self.replace(kwargs, True)

    @classmethod
    def load(cls, data, with_names=False):
        obj = object.__new__(cls)
        obj.replace(data, with_names)
        return obj

    def replace(self, data, with_names=False):
        for i, d in enumerate(self._struct_members):
            if with_names or type(data) is dict:
                v = d.load(data[d.name], with_names=with_names)
            else:
                v = d.load(data[i], with_names=with_names)
            setattr(self, d.name, v)

    def pack(self, with_names=False):
        if with_names:
            return {d.name: d.pack(getattr(self, d.name), with_names=with_names)
                for d in self._struct_members}
        else:
            return tuple(d.pack(getattr(self, d.name), with_names=with_names)
                for d in self._struct_members)

    def pack_bytes(self):
        import struct
        fmt = ''.join(m.fmt for m in self._struct_members)
        return struct.pack(fmt, *self.pack())


class Fields(object):
    @property
    def value(self):
        return Value()

    @property
    def int(self):
        return Int()

    @property
    def float(self):
        return Float()

    @property
    def str(self):
        return Str()

    @property
    def bytes(self):
        return Bytes()

    @property
    def bool(self):
        return Bool()

    def list(self, cls):
        return List(cls)

    def dict(self, keycls, valcls):
        return Dict(keycls, valcls)

    def child(self, reference):
        return Reference(reference)

field = Fields()
