import enum
import re

from pygenie.init import _make_initialized
_make_initialized()

from pygenie.init import S560_PATH

from pygenie.utils import extract_defines

DEFINE_REGEXP = r"\#define\s+(?P<symbol>[^\s]+)\s+(?P<value>[^\s]+)\s+"


# with rc.open() as f:
#     for m in  re.finditer(DEFINE_REGEXP, f.read()):
#         print(m.group("symbol") + " " + m.group("value"))

print(extract_defines(S560_PATH / 'SAD_RC.H', prefix="CSI_", required_names=["Error", "Okay"]))
