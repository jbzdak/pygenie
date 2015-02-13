from pygenie import init

init._make_initialized()

from pygenie.utils import extract_defines, hex_int, strip_int

pars = extract_defines(
    init.S560_PATH / 'CAMPDEF.H', prefix="CAM_",
    required_names=['L_CHANNELS'],
    value_mapper=hex_int)

text_lengths = dict(extract_defines(
    init.S560_PATH / 'CAM_N.H', prefix="CAM_N_",
    required_names=[],
    value_mapper=strip_int))

absolute_time_params = set()
# {
#     "X_ASTIME"
# }

par_map = dict(pars)
