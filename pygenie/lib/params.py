import enum
from http.client import UnimplementedFileMode
import pathlib
import configparser
import collections
import struct
from pygenie import init;
from pygenie.lib.errors import check_for_error

init._make_initialized()

from pygenie.resources import SAD_REPLACEMENTS

from pygenie.utils import IntAndDescriptionEnum, extract_defines, hex_int
from pygenie.utils.bitreader import BitReader


pars = extract_defines(
    init.S560_PATH / 'CAMPDEF.H', prefix="CAM_",
    required_names=['L_CHANNELS'],
    value_mapper=hex_int)

par_map = dict(pars)

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


class StructParamType(ParamType):

    # TODO: Untested

    def __init__(self, fmt):
        super().__init__()
        self.struct = struct.Struct(fmt)

    def get_field_size_in_bytes(self):
        raise NotImplementedError()

    def from_python(self, obj=None):
        size = self.struct.size
        to_ptr = init.ffi.new("char[]", size)
        size[:] = self.struct.pack(object)
        return to_ptr

    def to_python(self, pointer):
        return self.struct.unpack(pointer)

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

KNOWN_CHAR_PARAMETERS_LENGTHS = {
    'T_ECALTYPE': 8
}

def create_char_parameter_type(name):
    length = KNOWN_CHAR_PARAMETERS_LENGTHS.get(name)
    if length is None:
        return UnknownLengthTextParam(name)
    else:
        return FFITextParameter(length)

PARAM_TYPE_MAPPER = collections.defaultdict(lambda: lambda x: ParamType())

PARAM_TYPE_MAPPER.update({
    "L": lambda x: FFIParamType('LONG', 0, 4),
    "X": lambda x: FFIParamType('double', 0.0, 8),
    "T": create_char_parameter_type
})

Parameter = collections.namedtuple('Parameter', ['name', 'id', 'type'])

class ParamGenerator(object):
    
    def __getattr__(self, item):
        if item in self.__dict__: 
            return self.__dict__[item]
        param_id = par_map[item]
        par_type = PARAM_TYPE_MAPPER[item[0].upper()](item)
        return Parameter(item, param_id, par_type)
        
        
PARAM_GENERATOR = ParamGenerator()        

class ParamAlias(enum.Enum):

    NUMBER_OF_CHANNELS = PARAM_GENERATOR.L_CHANNELS
    TIME_LIVE = PARAM_GENERATOR.X_ELIVE
    TIME_REAL = PARAM_GENERATOR.X_EREAL

    ENERGY_CALIBRATION_TYPE = PARAM_GENERATOR.T_ECALTYPE


def get_parameter(dsc, parameter, record=1, entry=1):
    """
    A wrapper to SadGetParam
    :param dsc: Object obtained from create_vdm_connection
    :param parameter: Instance of ParamEnum or ParamAlias
    :param record: This is 1 based as in S650 library
    :param entry:
    :return:
    """
    if isinstance(parameter, ParamAlias):
        parameter = parameter.value
    pvalue = parameter.type.from_python()
    check_for_error(dsc, init.SAD_LIB.SadGetParam(
        dsc, parameter.id, record, entry,
        pvalue,
        parameter.type.get_field_size_in_bytes()))
    return pvalue[0]


def set_parameter(dsc, parameter, value,  record=1, entry=1):
    if isinstance(parameter, ParamAlias):
        parameter = parameter.value
    pvalue = parameter.type.from_python(value)
    check_for_error(dsc, init.SAD_LIB.SadPutParam(
        dsc, parameter.id, record, entry,
        pvalue,
        parameter.type.get_field_size_in_bytes()))


