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

class ParamType(object):

    def get_field_size_in_bytes(self):
        raise NotImplementedError()

    def from_python(self, obj=None):
        raise NotImplementedError()

    def to_python(self, pointer):
        raise NotImplementedError()

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

PARAM_TYPE_MAPPER = collections.defaultdict(lambda: ParamType())

PARAM_TYPE_MAPPER.update({
    "L": FFIParamType('LONG', 0, 4)
})


class ParamEnum(enum.Enum):

    def __init__(self, param_id, param_type):
        self.param_id = param_id
        self.param_type = param_type

Parameters = ParamEnum(
    "Parameters", names = [
        (n, (v, PARAM_TYPE_MAPPER[n[0].upper()]))
        for n, v in pars
    ]
)

class ParamAlias(enum.Enum):

    NUMBER_OF_CHANNELS = Parameters.L_CHANNELS

def get_parameter(dsc, parameter, record=0, entry=0):
    if isinstance(parameter, ParamAlias):
        parameter = parameter.value
    pvalue = parameter.param_type.from_python()
    check_for_error(dsc, init.SAD_LIB.SadGetParam(
        dsc, parameter.param_id, record+1, entry+1,
        pvalue,
        parameter.param_type.get_field_size_in_bytes()))
    return pvalue[0]


def set_parameter(dsc, parameter, value,  record, entry):
    if isinstance(parameter, ParamAlias):
        parameter = parameter.value
    pvalue = parameter.param_type.from_python(value)
    check_for_error(dsc, init.SAD_LIB.SadPutParam(
        dsc, parameter.param_id, record+1, entry+1,
        pvalue,
        parameter.param_type.get_field_size_in_bytes()))


