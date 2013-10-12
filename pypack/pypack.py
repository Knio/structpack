import sys

class PackType(object):
    __id = 0
    def __init__(self):
        PackType.__id += 1
        self.id = PackType.__id

    def __cmp__(self, other):
        return cmp(self.id, other.id)


class Bool(PackType):
    pass

class Int(PackType):
    pass

class Float(PackType):
    pass

class Str(PackType):
    pass

class List(PackType):
    pass

class Dict(PackType):
    pass

class MessageMeta(type):
    def __init__(cls, name, bases, dict):
        super(MessageMeta, cls).__init__(name, bases, dict)
        # collect attributes
        members = []
        for k, v in dict.iteritems():
            if isinstance(v, PackType):
                v.name = k
                members.append(v)
        members.sort()
        cls.pypack_members = members
        print cls, name, bases, dict


class Message(object):
    __metaclass__ = MessageMeta

    @classmethod
    def load(cls, data):
        obj = object.__new__(cls)
        for i, d in enumerate(cls.pypack_members):
            setattr(obj, d.name, data[i])
        return obj

    def pack(self):
        data = [getattr(self, d.name) for d in self.pypack_members]
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

data = Data()

