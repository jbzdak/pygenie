import pathlib
from pygenie import init
from pygenie.utils import IntAndDescriptionEnum

init._make_initialized()

import enum
from pygenie.init import  SAD_LIB, ffi

from pygenie.init import  ffi

class ErrorTypes(enum.IntEnum):
    Okay = 0
    Verify = 1

    Error = -1
    NoDSC = -2
    WrongState = -3

    @classmethod
    def is_error(cls, val):
        return val < 0

class OpenMode(enum.IntEnum):
    ReadOnly = 0
    ReadWrite = 1
    Exclusive = 2
    SysWrite = 4
    Direct = 128

class DetectorType(enum.IntEnum):
    Detector = 0x301
    CIF_NativeSpect = 1


class ErrorLevel(IntAndDescriptionEnum):
    HARDWARE_PROTOCOL_ERROR = (1, "Hardware Protocol driver error")
    VDM_DRIVER_ERROR = (2, "VDM Driver error")
    VDM_ERROR = (3, "VDM error")
    IPC_ERROR = (4, "IPC error")
    CLIENT_ERROR = (5, "Client (SAD access routine) error")
    APP_ERROR = (6, "Application error")

class ErrorClass(IntAndDescriptionEnum): 
    NONE=(0, "None, specific error value is sufficient")
    COMMAND_CLASS=(1, "Command class")
    HARDWARE_CLASS=(2, "Hardware class")
    COMM_CLASS=(3, "Communications class")
    OSS_CLASS=(4, "Operating system class")
    EVN_VAR_CLASS=(5, "Environment variable class.")
    DATA_CONVERSION_CLASS=(6, "Data conversion class")
    CAM_CLASS=(7, "CAM_CLASS")
    C_RUNTIME_CLASS=(8, "‘C’ runtime library class.");



class ConnectorException(Exception):
    pass

class ConnectorError(Exception):
    """
    Some function returned CSI_Error error

    TODO: You can get error details using SadGetStatus but
    I'll try to not impkement it.
    """


class ConnectorNoDsc(ConnectorException):
    """
    Some function returned CSI_NoDSC error
    """

class ConnectorWrongState(ConnectorException):
    """
    Some C function returned CSI_WrongState error.

    This one means that some function was called out of sequence
    """

class ConnectorVerifyError(ConnectorException):
    """
    Some C function returned CSI_Verify error.

    I'm not sure whether this is an error or a warining, so will treat it as error.
    """


def check_for_error(dsc, result_value):
    if result_value == ErrorTypes.Okay:
        return
    if result_value == ErrorTypes.Verify:
        raise ConnectorVerifyError()
    if result_value == ErrorTypes.NoDSC:
        raise ConnectorNoDsc()
    if result_value == ErrorTypes.WrongState:
        raise ConnectorWrongState()
    if result_value == ErrorTypes.Error:
        raise ConnectorError(dsc)

def delete_vdm_connection(dsc):
    SAD_LIB.SadDeleteDSC(dsc)

def open_source(dsc, source_location, detector_type, open_mode, verify_hardware=False, shell_id=b""):

    if isinstance(source_location, str):
        source_location = pathlib.Path(source_location)

    check_for_error(dsc, SAD_LIB.SadOpenDataSource(dsc, bytes(source_location), detector_type, open_mode, verify_hardware, shell_id))

def create_vdm_connection():
    dsc = init.ffi.new("void**")
    #Yes these arguments myst allways be zero
    try:
        check_for_error(dsc, SAD_LIB.iUtlCreateFileDSC2(dsc, 0, ffi.NULL))
    except ConnectorError:
        delete_vdm_connection(dsc) # In case of this error we are responsible for deleting dsc
        raise

    return dsc[0]
