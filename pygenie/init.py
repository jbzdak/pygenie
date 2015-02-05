import numpy as np
from cffi import FFI
import pathlib

from pygenie import resources

S560_PATH = None
SAD_LIB = None
INITIALIZED = False

def _make_initialized():
    if not INITIALIZED:
        initialize()

def initialize(s560_path="C:\GENIE2K\S560"):
    global S560_PATH, SAD_LIB, INITIALIZED
    if INITIALIZED:
        raise ValueError("Already initialized using '{}' path".format(S560_PATH))

    S560_PATH = pathlib.Path(s560_path)
    S560_PATH_STR = str(S560_PATH)

    S560_LIBS = [str(lib.stem) for lib in S560_PATH.iterdir() if lib.suffix.lower() == '.lib']


    ffi = FFI()
    ffi.cdef(resources.get_cdef())

    SAD_LIB = ffi.verify(resources.get_includes(), libraries=S560_LIBS+resources.get_system_libs(), include_dirs=[S560_PATH_STR], library_dirs=[S560_PATH_STR])

    SAD_LIB.vG2KEnv()
    INITIALIZED=True