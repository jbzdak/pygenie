from pygenie.init import _make_initialized; _make_initialized()

from pygenie.utils import extract_defines, hex_int

from pygenie.init import S560_PATH

pars = extract_defines(
    S560_PATH / 'CAMPDEF.H', prefix="CAM_", required_names=[],
    value_mapper=hex_int)

print (len(pars))
