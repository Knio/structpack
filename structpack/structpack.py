
class PackType(object):
    __id = 0
    def __init__(self):
        PackType.__id += 1
        self.id = PackType.__id

    def __cmp__(self, other):
        return cmp(self.id, other.id)


class PrimitiveType(PackType):
    @staticmethod
    def load(a, **kwargs):
        return a

    @staticmethod
    def pack(a, **kwargs):
        return a


class Bool(PrimitiveType):
    pass

class Int(PrimitiveType):
    pass

class Float(PrimitiveType):
    pass

class Str(PrimitiveType):
    pass


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
            for k, v in a.iteritems()}

    def pack(self, a, **kwargs):
        return {self.keycls.pack(k, **kwargs): self.valcls.pack(v, **kwargs)
            for k, v in a.iteritems()}


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
        for k, v in dict.iteritems():
            if isinstance(v, PackType):
                v.name = k
                members[k] = v
        cls._struct_members = sorted(members.values())


class Message(object):
    __metaclass__ = MessageMeta

    @classmethod
    def load(cls, data, with_names=False):
        obj = object.__new__(cls)
        for i, d in enumerate(cls._struct_members):
            if with_names or type(data) is dict:
                v = d.load(data[d.name], with_names=with_names)
            else:
                v = d.load(data[i], with_names=with_names)
            setattr(obj, d.name, v)
        return obj

    def pack(self, with_names=False):
        if with_names:
            return {d.name: d.pack(getattr(self, d.name), with_names=with_names)
                for d in self._struct_members}
        else:
            return tuple(d.pack(getattr(self, d.name), with_names=with_names)
                for d in self._struct_members)


class Data(object):
    __version__ = '1.1.0'
    msg = Message

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
    def bool(self):
        return Bool()

    def list(self, cls):
        return List(cls)

    def dict(self, keycls, valcls):
        return Dict(keycls, valcls)

    def child(self, reference):
        return Reference(reference)

data = Data()
