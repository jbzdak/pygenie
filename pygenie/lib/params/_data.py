import enum
from http.client import UnimplementedFileMode
import pathlib
import configparser
import collections
import struct
from pygenie import init;
from pygenie.lib.errors import check_for_error

init._make_initialized()

from pygenie.resources import SAD_REPLACEMENTS

from pygenie.utils import IntAndDescriptionEnum, extract_defines, hex_int, strip_int
from pygenie.utils.bitreader import BitReader


pars = extract_defines(
    init.S560_PATH / 'CAMPDEF.H', prefix="CAM_",
    required_names=['L_CHANNELS'],
    value_mapper=hex_int)

text_lengths = dict(extract_defines(
    init.S560_PATH / 'CAM_N.H', prefix="CAM_N_",
    required_names=[],
    value_mapper=strip_int))

par_map = dict(pars)
