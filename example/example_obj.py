__author__ = 'jb'


import numpy as np

from pygenie import init; init.initialize()

from pygenie.pygenie import PYGenieObj, open_cam_source, SourceType

with open_cam_source("C:\\GENIE2K\\CAMFILES\\nbsstd.CNF", SourceType.NativeSpect) as src:
    assert isinstance(src, PYGenieObj)
    print("Source count", src.channel_count)
    print("Acquisition sart time", src.measurement_start_time)
    print("Sample ID", src.sample_id)
    print("Measurement time", src.measurement_time)
    print("Energy calibration coeffs", src.energy_calibration.get_calibration_coefficients())
    coeffs = src.energy_calibration.get_calibration_coefficients()
    print("Energy in channels", np.polyval(coeffs, np.arange(1, src.channel_count)))
    print("Spectrum", src[:])
    print("Spectrum", src[30:50])

