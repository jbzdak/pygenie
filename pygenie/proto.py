import numpy as np
import cffi

import pathlib

S560_PATH = pathlib.Path("C:\GENIE2K\S560")
S560_PATH_STR = str(S560_PATH)

S560_LIBS = [str(lib.stem) for lib in S560_PATH.iterdir() if lib.suffix.lower() == '.lib']

SYSTEM_LIBS = [s.split(".")[0] for s in """
kernel32.lib
user32.lib
gdi32.lib
winspool.lib
comdlg32.lib
advapi32.lib
shell32.lib
ole32.lib
oleaut32.lib
uuid.lib
odbc32.lib
odbccp32.lib
""".strip().split()]

INCLUDE_PATTERN = """

"""
from cffi import FFI

ffi = FFI()
ffi.cdef("""
#include <crackers.h>
#include <citypes.h>
void vG2KEnv( void );
int iUtlCreateFileDSC2( HMEM  * phDSC, BOOL fAdvise, HWND hAdvise );
""")

C = ffi.verify(INCLUDE_PATTERN.format(S560_PATH=S560_PATH), libraries=S560_LIBS+SYSTEM_LIBS, include_dirs=[S560_PATH_STR], library_dirs=[S560_PATH_STR])

C.vG2KEnv()

print("Done")