import pathlib

from pygenie import init;

init._make_initialized()
from pygenie.utils import extract_defines, hex_int

from pygenie.lib.errors import check_for_error, ReturnErrorCodes

import enum


SourceType = enum.IntEnum(
    "SourceType",
    extract_defines(init.S560_PATH / 'CI_FILES.H', prefix="CIF_",
                    required_names=["NativeSpect", "Detector"], value_mapper=hex_int))

OpenFlags = enum.IntEnum(
    "OpenFlags", extract_defines(
        init.S560_PATH / 'Spasst.h', prefix="ACC_", value_mapper=hex_int,
        required_names=["ReadOnly", "ReadWrite", "Exclusive", 'SysWrite', 'AppWrite', 'Direct']))


def delete_vdm_connection(dsc):
    check_for_error(dsc, init.SAD_LIB.SadDeleteDSC(dsc))

def open_source(dsc, source_location, detector_type, open_mode, verify_hardware=False, shell_id=b""):

    if isinstance(source_location, str):
        source_location = pathlib.Path(source_location)

    check_for_error(dsc, init.SAD_LIB.SadOpenDataSource(dsc, bytes(source_location), int(detector_type), int(open_mode), verify_hardware, shell_id))

def create_vdm_connection():
    dsc = init.ffi.new("void**")
    #Yes these arguments myst allways be zero
    needs_to_delete_dsc = False

    # This is ankward error handling, but here is the rationale
    # If iUtlCreateFileDSC2 returns Error we need to manally delete DSC,
    # This should be done even if some other exception is raised
    # (for example while getting error details)
    init_result = init.SAD_LIB.iUtlCreateFileDSC2(dsc, 0, init.ffi.NULL)
    dsc = dsc[0]
    if init_result == ReturnErrorCodes.Error:
        needs_to_delete_dsc = True
    try:
        check_for_error(dsc, init_result)
    finally:
        if needs_to_delete_dsc:
            delete_vdm_connection(dsc) # In case of this error we are responsible for deleting dsc

    return dsc

def flush(dsc):
    init.SAD_LIB.SadFlush(dsc)

# def get_spectral_data(dsc, channel)