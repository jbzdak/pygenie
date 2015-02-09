
import enum

import numpy as np

from pygenie import init;
from pygenie.lib.errors import check_for_error
from pygenie.resources import SAD_REPLACEMENTS, MAX_NUMBER_OF_SPECTRUM_CHANNELS_IN_CALL

init._make_initialized()

class SpectrumType(enum.Enum):

    FLOAT_DATA = (1, SAD_REPLACEMENTS['REAL'], np.float32)
    LONG_DATA =  (0, SAD_REPLACEMENTS['ULONG'], np.uint32)


def _get_spectrum_simple(dsc, channel_from, channel_to, spectrum_type=SpectrumType.LONG_DATA):
    chanel_count = channel_to - channel_from
    if chanel_count > MAX_NUMBER_OF_SPECTRUM_CHANNELS_IN_CALL:
        raise ValueError("To many channels")

    result_data = np.ndarray(chanel_count, dtype=spectrum_type.value[2])

    ptr = init.ffi.from_buffer(result_data)

    check_for_error(dsc, init.SAD_LIB.SadGetSpectrum(
        dsc, channel_from+1, channel_to+1, spectrum_type.value[0], ptr))

    return result_data


