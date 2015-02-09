import pathlib
import configparser
import collections
from pygenie import init; init._make_initialized()

from pygenie.resources import SAD_REPLACEMENTS

from pygenie.utils import IntAndDescriptionEnum, extract_defines
from pygenie.utils.bitreader import BitReader

import enum

error_messages = pathlib.Path(__file__).parent / "known_error_messages.ini"

ERROR_MESSAGES = configparser.ConfigParser()
with error_messages.open() as f:
    ERROR_MESSAGES.read_file(f)

ReturnErrorCodes = enum.IntEnum(
    "ReturnErrorCodes",
    extract_defines(init.S560_PATH / 'SAD_RC.H', prefix="CSI_", required_names=["Error", "Okay"]))

class ErrorLevel(IntAndDescriptionEnum):
    # This seems to be only defined in the doc
    NONE = (1, "Unknown?")
    HARDWARE_PROTOCOL_ERROR = (1, "Hardware Protocol driver error")
    VDM_DRIVER_ERROR = (2, "VDM Driver error")
    VDM_ERROR = (3, "VDM error")
    IPC_ERROR = (4, "IPC error")
    CLIENT_ERROR = (5, "Client (SAD access routine) error")
    APP_ERROR = (6, "Application error")

class ErrorClass(IntAndDescriptionEnum):
    # This seems to be only defined in the doc
    NONE=(0, "None, specific error value is sufficient")
    COMMAND_CLASS=(1, "Command class")
    HARDWARE_CLASS=(2, "Hardware class")
    COMM_CLASS=(3, "Communications class")
    OSS_CLASS=(4, "Operating system class")
    EVN_VAR_CLASS=(5, "Environment variable class.")
    DATA_CONVERSION_CLASS=(6, "Data conversion class")
    CAM_CLASS=(7, "CAM_CLASS")
    C_RUNTIME_CLASS=(8, "‘C’ runtime library class.")

class GenieException(Exception):
    pass

class GenieError(GenieException):
    def __init__(self, dsc, error_code):
        self.error_code = error_code
        self.error = None
        if error_code == ReturnErrorCodes.Error:
            self.error = get_and_unpack_error(dsc)
        super().__init__(error_code, self.error)

class GenieSadGetStatusError(GenieException):
    pass

def is_sad_call_successful(result_value):
    return result_value == ReturnErrorCodes.Okay

def check_for_error(dsc, result_value):
    if is_sad_call_successful(result_value):
        return
    raise GenieError(dsc, result_value)

ErrorStatus = collections.namedtuple(
    "ErrorStatus", ['error_detail', 'error_level', 'error_class', 'error_message'])

def _sad_get_status(dsc):
    error_code = init.ffi.new("{}*".format(SAD_REPLACEMENTS['ULONG']))
    zero_a = init.ffi.new("short*")
    zero_b = init.ffi.new("{}*".format(SAD_REPLACEMENTS['USHORT']))
    zero_a[0] = zero_b[0] = 0

    result = init.SAD_LIB.SadGetStatus(dsc, error_code, zero_a, zero_b)

    if not is_sad_call_successful(result):
        raise GenieSadGetStatusError()

    return error_code[0]

def unpack_error(error_code):
    """
    >>> res = unpack_error(int('278e2a', 16))
    >>> res.error_detail == '8e2a'
    True
    >>> res.error_level == ErrorLevel.VDM_DRIVER_ERROR
    True
    >>> res.error_class == ErrorClass.CAM_CLASS
    True

    :param error_code:
    :return:
    """

    # Behold innovative way to handle bitsets in Python
    err_string = "{0:b}".format(error_code)

    error_bitfield = (32 - len(err_string)) * '0' + err_string

    error_detail = int(error_bitfield[-16:], 2)
    error_class = ErrorClass.by_index(int(error_bitfield[-20:-16], 2))
    error_level = ErrorLevel.by_index(int(error_bitfield[-27:-20], 2))
    error_message = ERROR_MESSAGES.get(
        'Errors',
        '{:x}'.format(error_detail),
        fallback=ERROR_MESSAGES.get('Errors', 'default')
    )



    return ErrorStatus(
        '{:x}'.format(error_detail),
        error_level,
        error_class,
        error_message
    )

def get_and_unpack_error(dsc):
    err = _sad_get_status(dsc)

    return unpack_error(err)




