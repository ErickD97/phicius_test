import operator
from collections import OrderedDict

from django.db import models


class EnumMetaClass(type):
    __choices__ = OrderedDict()

    def __init__(cls, name, bases, classdict):
        def _human_enum_values(enum):
            return cls.__choices__[enum]

        cls.humanize = _human_enum_values
        super().__init__(name, bases, classdict)

    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, name, bases, classdict):
        attributes = []
        keys = {}
        choices = OrderedDict()
        for key, value in classdict.items():
            if key.startswith("__"):
                continue
            attributes.append(key)
            if isinstance(value, tuple):
                value, alias = value
                keys[alias] = key
            else:
                alias = None
            keys[alias or key] = key
            choices[alias or key] = value

        for k, v in keys.items():
            classdict[v] = k

        classdict["__choices__"] = choices
        classdict["__attributes__"] = attributes

        classdict["choices"] = tuple((str(k), str(v)) for k, v in choices.items())

        return type.__new__(cls, name, bases, classdict)


class Enum(metaclass=EnumMetaClass):
    pass
