import collections
import enum

from pygenie import init; init._make_initialized()

from pygenie.lib.params._data import par_map, pars, text_lengths

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


class FFITextParameter(ParamType):

    def __init__(self, text_len):
        super().__init__()
        self.text_len = text_len
        self.default = b' '*self.text_len

    def from_python(self, obj=None):

        if obj is None:
            obj = self.default

        obj = b' ' * (self.text_len - len(obj)) + obj

        value = init.ffi.new('char[]', self.text_len)

        value[0:self.text_len] = obj
        return value

    def get_field_size_in_bytes(self):
        return self.text_len

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
    "X": lambda x: FFIParamType('double', 0.0, 8),
    "F": lambda x: FFIParamType('float', 0.0, 4),
    "T": create_char_parameter_type})

Parameter = collections.namedtuple('Parameter', ['name', 'id', 'type'])

class ParamGenerator(object):

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        param_id = par_map[item]
        par_type = PARAM_TYPE_MAPPER[item[0].upper()](item)
        return Parameter(item, param_id, par_type)


PARAM_GENERATOR = ParamGenerator()

class ParamAliasBase(enum.Enum):

    @property
    def param(self):
        return getattr(PARAM_GENERATOR, self.value)