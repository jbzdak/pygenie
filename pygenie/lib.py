
from pygenie import init
init._make_initialized()
from pygenie.init import  SAD_LIB, ffi

from pygenie.resources import ErrorTypes
from pygenie.init import  ffi

import cffi


class ConnectorException(Exception):
    pass

class ConnectorError(Exception):
    """
    Some function returned CSI_Error error
    """

    def __init__(self, dsc, *args, **kwargs):
        super().__init__(*args, **kwargs)


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

def create_vdm_connection():
    dsc = init.ffi.new("void**")
    #Yes these arguments myst allways be zero
    try:
        check_for_error(dsc, SAD_LIB.iUtlCreateFileDSC2(dsc, 0, 0))
    except ConnectorError:
        delete_vdm_connection(dsc) # In case of this error we are responsible for deleting dsc
        raise

    return dsc[0]
