import numpy as np
import cffi

import pathlib

S560_PATH = pathlib.Path("C:\GENIE2K\S560")

S560_LIBS = [str(lib.absolute()) for lib in S560_PATH.iterdir() if lib.suffix.lower() == '.lib']

INCLUDE_PATTERN = """

/* Windows includes */

#include <windows.h>
#include "{S560_PATH}/crackers.h"

/* C run time library includes */

#include <tchar.h>
#include <stdio.h>


/* GENIE-PC User Library includes */

#include "{S560_PATH}/citypes.h"

#include "{S560_PATH}/spasst.h"
#include "{S560_PATH}/sad.h"
#include "{S560_PATH}/ci_files.h"
#include "{S560_PATH}/campdef.h"
#include "{S560_PATH}/cam_n.h"


/* GENIE-PC Utility Library includes */

#include "{S560_PATH}/utility.h"
"""

print(S560_LIBS)

from cffi import FFI

ffi = FFI()
ffi.cdef("""
    void vG2KEnv( void );
""")
C = ffi.verify(INCLUDE_PATTERN.format(S560_PATH=S560_PATH), libraries=S560_LIBS, include_dirs=[S560_PATH])