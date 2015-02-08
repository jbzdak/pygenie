
import pathlib
import enum

RES_DIR = pathlib.Path(__file__).parent

_SAD_REPLACEMENTS = [
    ['HMEM', "void*"],
    ['BOOL', 'int'],
    ['HWND', "void*"],
    ['SADENTRY', 'short'],
    ['USHORT', 'unsigned short'],
    ["FLAG", 'unsigned int'],
    ['ULONG', 'unsigned int'],
    ['UINT', 'unsigned int']
]

SAD_REPLACEMENTS = dict(_SAD_REPLACEMENTS)

def get_includes():
    with RES_DIR.joinpath('cffi_includes.c').open() as f:
        return f.read()

def get_cdef():
    """
    This will be passed to cffi.cdef, this is copy-pasted from Genie
    header files --- so I'll unwap ankward defines and typedefs
    so cffi understands datatypes.
    :return:
    """
    with RES_DIR.joinpath('cffi_cdef.c').open() as f:
        RAW = f.read()

    assert isinstance(RAW, str)
    for (src, dst) in _SAD_REPLACEMENTS:
        RAW = RAW.replace(src, dst)

    return RAW

def get_system_libs():
    with RES_DIR.joinpath('system_libs.txt').open() as f:
        RAW = f.read()
    return [s.split('.')[0] for s in RAW.strip().split()]

print(get_cdef())
