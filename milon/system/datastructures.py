import re
import collections

from collections import OrderedDict


class SortedDict(OrderedDict):

    @property
    def keyOrder(self):
        return list(self.keys())

    def insert(self, index, key, value):
        self[key] = value
        self[key] = value
        for ii, k in enumerate(list(self.keys())):
            if ii >= index and k != key:
                self.move_to_end(k)


class SimpleEnum(object):


    def __extract(self, src, field, default):
        ret = src.get(field)
        if ret != None:
            src.__delitem__(field)
        else:
            ret = default
        return ret

    def __init__(self, *keys, **kwargs):
        """ Create an enumeration instance """
        # next_value function
        next_value = self.__extract(kwargs, 'next_value', lambda x: x + 1)
        # key_type type
        value_type = self.__extract(kwargs, 'value_type', EnumValue)
        # key_type type
        key_type = self.__extract(kwargs, 'key_type', int)
        # start_from value
        start_from = self.__extract(kwargs, 'start_from', 1)
        employee_type_config = self.__extract(kwargs, 'employee_type_config', False)
        super(SimpleEnum, self).__setattr__('_empty_value', self.__extract(kwargs, 'empty_value', ''))
        super(SimpleEnum, self).__setattr__('_empty_text', self.__extract(kwargs, 'empty_text', ''))
        super(SimpleEnum, self).__setattr__('_sorted', SortedDict())

        values = {}
        if keys:
            # key is the accessor
            # index is saved in database
            # value is the display value
            keys = tuple(keys)

            index = start_from
            for key in keys:
                enum_value = value_type(self, index, key)
                values[index] = enum_value
                self._sorted[index] = enum_value.label
                index = next_value(index)
                super(SimpleEnum, self).__setattr__(key, enum_value)
        elif kwargs:
            keys = tuple(kwargs)

            for key, index in kwargs.items():
                enum_value = value_type(self, index, key)
                values[index] = enum_value
                self._sorted[index] = enum_value.label
                super(SimpleEnum, self).__setattr__(key, enum_value)
        else:
            raise EnumEmptyError()

        super(SimpleEnum, self).__setattr__('_keys', keys)
        super(SimpleEnum, self).__setattr__('_values', values)
        super(SimpleEnum, self).__setattr__('_key_type', key_type)
        super(SimpleEnum, self).__setattr__('_value_type', value_type)
        super(SimpleEnum, self).__setattr__('_employee_type_config', employee_type_config)

    def __setattr__(self, name, value):
        raise EnumImmutableError(name)

    def __delattr__(self, name):
        raise EnumImmutableError(name)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, index):
        return self._values[int(index) if isinstance(index, str) and index.isdigit() else index]

    def __setitem__(self, index, value):
        raise EnumImmutableError(index)

    def __delitem__(self, index):
        raise EnumImmutableError(index)

    def __iter__(self):
        return iter(self._values)

    def getValue(self, key):
        for v in self._values.values():
            if v.key == key:
                return v
        raise EnumBadKeyError(key)

    def get(self, key, d=None):
        try:
            v = self[key]
            return v
        except:
            return d

    def _insert_empty_item(self, sorted_dict, empty=False, all=False):
        if empty:
            sorted_dict.insert(0, self._empty_value, self._empty_text)
        elif all:
            sorted_dict.insert(0, self._empty_value, 'All')
        return sorted_dict

    def dict(self, start=None, end=None, ignore=(), empty=False, all=False, title_form=False, dont_insert_space=False,
             values_in=()):
        if isinstance(ignore, str) or not isinstance(ignore, collections.abc.Iterable):
            ignore = [ignore]
        if values_in and isinstance(values_in, str) or not isinstance(values_in, collections.abc.Iterable):
            values_in = [values_in]
        if start is not None:
            start = self._sorted.keyOrder.index(start)
        if end is not None:
            end = self._sorted.keyOrder.index(end) + 1

        new_dict = SortedDict()
        self._insert_empty_item(new_dict, empty=empty, all=all)
        for k, v in list(self._sorted.items())[start:end]:
            if k not in ignore:
                v = v.replace('_', ' ') if title_form else v
                new_dict[k] = v
                if dont_insert_space:
                    new_dict[k] = new_dict.get(k, '').replace(' ', '')

        return new_dict

    def __contains__(self, index):
        return (int(index) if isinstance(index, str) else index) in self._values


class EnumValue(object):
    _decamel = re.compile(r'[A-Z]*[^A-Z]*')

    """ A specific value of an enumerated type """

    def __init__(self, enumtype, index, key):
        """ Set up a new instance """
        self.__enumtype = enumtype
        self.__index = index
        self.__key = key
        self.__label = ' '.join([_f for _f in self._decamel.findall(str(self)) if _f])

    @property
    def enumtype(self):
        return self.__enumtype

    @property
    def label(self):
        return self.__label

    @property
    def key(self):
        return self.__key

    @property
    def index(self):
        return self.__index

    def __str__(self):
        return "%s" % (self.key)

    def __int__(self):
        return int(self.index)

    def __repr__(self):
        return "EnumValue(%s, %s, %s)" % (
            repr(self.__enumtype),
            repr(self.__index),
            repr(self.__key),
        )

    def __hash__(self):
        return hash(self.__index)

    def _process_other_val(self, other):
        return other.index if isinstance(other, EnumValue) else (type(self.index)(other) if other else '')

    def __lt__(self, other):
        return self.index < self._process_other_val(other)

    def __le__(self, other):
        return self.index <= self._process_other_val(other)

    def __gt__(self, other):
        return self.index > self._process_other_val(other)

    def __ge__(self, other):
        return self.index >= self._process_other_val(other)

    def __eq__(self, other):
        return self.index == self._process_other_val(other)

    def __ne__(self, other):
        return self.index != self._process_other_val(other)
