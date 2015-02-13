from _operator import itemgetter
import collections
import enum
import re

from pygenie import init;
from pygenie.init import SAD_LIB
from pygenie.lib.errors import GenieDatetimeConversionError

init._make_initialized()

from pygenie.lib.params._data import par_map, text_lengths, absolute_time_params

class ParamType(object):

    def get_field_size_in_bytes(self):
        raise NotImplementedError()

    def from_python(self, obj=None):
        raise NotImplementedError()

    def to_python(self, pointer):
        raise NotImplementedError()

class UnsupportedParam(ParamType):

    def __init__(self, param_type):
        self.param_type = param_type

    def get_field_size_in_bytes(self):
        raise NotImplementedError("Unsupported (yet) param type '{}'".format(self.param_type))

    def from_python(self, obj=None):
        raise NotImplementedError("Unsupported (yet) param type '{}'".format(self.param_type))

    def to_python(self, pointer):
        raise NotImplementedError("Unsupported (yet) param type '{}'".format(self.param_type))

class UnknownLengthTextParam(ParamType):

    def __init__(self, param_name):
        self.param_name = param_name

    def get_field_size_in_bytes(self):
        raise NotImplementedError("Text parameter {} has unknown length, and can't be used".format(self.param_name))

    def from_python(self, obj=None):
        raise NotImplementedError("Text parameter {} has unknown length, and can't be used".format(self.param_name))

    def to_python(self, pointer):
        raise NotImplementedError("Text parameter {} has unknown length, and can't be used".format(self.param_name))

class FFIParamType(ParamType):
    def __init__(self, ffi_type, default, object_size):
        super().__init__()
        self.ffi_type = ffi_type
        self.default = default
        self.object_size = object_size

    def get_field_size_in_bytes(self):
        return self.object_size


    def from_python(self, obj=None):
        if obj is None:
            obj=self.default
        ptr = init.ffi.new("{}*".format(self.ffi_type))
        ptr[0] = obj
        return ptr

    def to_python(self, pointer):
        return pointer[0]

class TimeDeltaParam(FFIParamType):
    def __init__(self):
        super().__init__('double', 0.0, 8)


class FFITextParameter(ParamType):

    def __init__(self, text_len):
        super().__init__()
        self.text_len = text_len-1
        self.string_len = text_len
        self.default = b'-'*self.text_len

    def from_python(self, obj=None):

        if obj is None:
            obj = self.default

        if len(obj) > self.text_len:
            raise ValueError("Value of parmeter is longer than field length")

        obj = obj + b'\0' * (self.string_len - len(obj))

        value = init.ffi.new('char[]', self.string_len)

        value[0:self.string_len] = obj
        return value

    def get_field_size_in_bytes(self):
        return self.string_len

    def to_python(self, pointer):
        return init.ffi.string(pointer)

def create_char_parameter_type(name):
    length = text_lengths[name[2:]]
    if length is None:
        return UnknownLengthTextParam(name)
    else:
        return FFITextParameter(length)

PARAM_TYPE_MAPPER = collections.defaultdict(lambda: lambda x: ParamType())

PARAM_TYPE_MAPPER.update({
    "L": lambda x: FFIParamType('LONG', 0, 4),
    "X": lambda x: TimeDeltaParam(),
    "F": lambda x: FFIParamType('float', 0.0, 4),
    "T": create_char_parameter_type})

Parameter = collections.namedtuple('Parameter', ['name', 'id', 'type'])

def _parameter_type_for_name( param_name):
    return PARAM_TYPE_MAPPER[param_name[0].upper()](param_name)

class SerialParam(object):

    @classmethod
    def _create_from_matches(cls, matches):
        def par_from_match(match):
            return Parameter(
                match[0], match[1], _parameter_type_for_name(match[0])
            )
        return SerialParam(
            par_from_match(matches[0]),
            {m[2]:par_from_match(m) for m in matches}
        )

    def __init__(self, first_param, param_map):
        self.name, self.id, self.type = first_param
        self.param_map = param_map

    def __getitem__(self, item):
        return self.param_map[item]

    def __len__(self):
        return len(self.param_map)

    def __iter__(self):
        return iter((self.param_map[ii] for ii in sorted(self.param_map.keys())))

class ParamGenerator(object):

    def __init__(self):
        super().__init__()
        self.__serial_params_cache = {}

    def param_set(self):
        return par_map.keys()

    def __getattr__(self, item):
        try:
            param_id = par_map[item]
        except KeyError:
            raise AttributeError(item)
        par_type = _parameter_type_for_name(item)
        p = Parameter(item, param_id, par_type)
        setattr(self, item, p)
        return p

    def __getitem__(self, item):
        return self.__getattr__(item)

    def get_serial_parametr(self, item_pattern):
        if item_pattern in self.__serial_params_cache:
            return self.__serial_params_cache[item_pattern]
        search_format = re.compile(item_pattern.format(r"(?P<param_idx>\d+)"))
        matches = []
        for name, value in par_map.items():
            m = re.match(search_format, name)
            if m:
                matches.append((name, value, int(m.group('param_idx'))))
        matches = sorted(matches, key=itemgetter(2))
        return SerialParam._create_from_matches(matches)

    def get_composite_parameter(self, param_names):
        return SerialParam._create_from_matches(
            [(param, par_map[param], ii) for ii, param in enumerate(param_names) ]
        )

PARAM_GENERATOR = ParamGenerator()

class ParamAliasBase(enum.Enum):

    @property
    def param(self):
        return getattr(PARAM_GENERATOR, self.value)

    def __getitem__(self, item):
        return self.value[item]

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)