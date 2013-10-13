import sys

class PackType(object):
    __id = 0
    def __init__(self):
        PackType.__id += 1
        self.id = PackType.__id

    def __cmp__(self, other):
        return cmp(self.id, other.id)

    @staticmethod
    def load(a):
        return a

    @staticmethod
    def pack(a):
        return a


class Bool(PackType):
    pass

class Int(PackType):
    pass

class Float(PackType):
    pass

class Str(PackType):
    pass

class List(PackType):
    def __init__(self, cls):
        PackType.__init__(self)
        self.cls = cls

    def load(self, a):
        return list(self.cls.load(i) for i in a)

    def pack(self, a):
        return tuple(self.cls.pack(i) for i in a)

class Dict(PackType):
    def __init__(self, keycls, valcls):
        PackType.__init__(self)
        self.keycls = keycls
        self.valcls = valcls

    def load(self, a):
        return {self.keycls.load(k): self.valcls.load(v) for k, v in a.iteritems()}

    def pack(self, a):
        return {self.keycls.pack(k): self.valcls.pack(v) for k, v in a.iteritems()}

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
        members = []
        for k, v in dict.iteritems():
            if isinstance(v, PackType):
                v.name = k
                members.append(v)
            elif type(v) is MessageMeta:
                r = Reference(v)
                r.name = k
                members.append(r)
        members.sort()
        cls.pypack_members = members
        print cls, name, bases, dict


class Message(object):
    __metaclass__ = MessageMeta

    @classmethod
    def load(cls, data):
        obj = object.__new__(cls)
        for i, d in enumerate(cls.pypack_members):
            setattr(obj, d.name, d.load(data[i]))
        return obj

    def pack(self):
        data = tuple(d.pack(getattr(self, d.name)) for d in self.pypack_members)
        return data


class Data(object):
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

data = Data()

