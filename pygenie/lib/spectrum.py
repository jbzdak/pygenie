
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

    ptr = init.ffi.new("{}[]".format(spectrum_type.value[1]), chanel_count)

    check_for_error(dsc, init.SAD_LIB.SadGetSpectrum(
        dsc, channel_from+1, chanel_count, spectrum_type.value[0], ptr))

    tmp_data = np.frombuffer(init.ffi.buffer(ptr), dtype=spectrum_type.value[2], count=chanel_count)

    result = np.array(tmp_data, copy=True)

        # result = np.zeros(chanel_count, spectrum_type.value[2])

    # for ii in range(chanel_count):
    #     result[ii] = ptr[ii]

    del tmp_data
    del ptr

    return result

def get_spectrum(dsc, channel_from, channel_to, spectrum_type=SpectrumType.LONG_DATA):
    chanel_count = channel_to - channel_from
    arrays = []
    curr_from = channel_from
    while curr_from < channel_to:
        arrays.append(
            _get_spectrum_simple(
                dsc, curr_from, min(channel_to, curr_from+MAX_NUMBER_OF_SPECTRUM_CHANNELS_IN_CALL),
                spectrum_type=spectrum_type)
        )
        curr_from+=MAX_NUMBER_OF_SPECTRUM_CHANNELS_IN_CALL
    return np.hstack(arrays)