import operator
from collections import OrderedDict

from django.db import models


class FieldDeconstructMixin:
    IGNORED_ATTRS = [
        "verbose_name",
        "help_text",
        "choices",
        "get_latest_by",
        "ordering",
    ]

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        for attr in self.IGNORED_ATTRS:
            kwargs.pop(attr, None)
        return name, path, args, kwargs


class EnumMetaClass(type):
    __choices__ = OrderedDict()

    def __init__(cls, name, bases, classdict):
        def _human_enum_values(enum):
            return cls.__choices__[enum]

        # add a class attribute
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

        # sort using reverse so that they appear in the declared order
        classdict["choices"] = tuple((str(k), str(v)) for k, v in choices.items())

        return type.__new__(cls, name, bases, classdict)


class Enum(metaclass=EnumMetaClass):
    pass


class CustomEnumField(FieldDeconstructMixin, models.CharField):
    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        choices = enum.choices
        defaults = {"choices": choices, "max_length": max(len(k) for k, v in choices)}
        defaults.update(kwargs)
        super().__init__(*args, **defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["enum"] = self.enum
        return name, path, args, kwargs
