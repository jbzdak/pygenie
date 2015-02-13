from uuid import uuid4

import re

import numpy as np

import datetime
import time

from pygenie.init import initialize;
from pygenie import init
from pygenie.lib.errors import GenieError
from pygenie.lib.params import SampleDescription
from pygenie.lib.params._par_type import PARAM_GENERATOR, convert_interval_to_absolute_date

from pygenie.lib import create_vdm_connection, delete_vdm_connection, open_source, OpenFlags, SourceType, flush
from pygenie.lib import params
from pygenie.lib import spectrum

import datetime

conn = create_vdm_connection()

open_source(conn,  "C:\\GENIE2K\\CAMFILES\\nbsstd.CNF", SourceType.NativeSpect, OpenFlags.ReadOnly|OpenFlags.ReadWrite)

# Parameter reading is easy, but there are many ways to obtain parameter object
# All defined parameters are avilable from PARAM_GENERATOR object
# Parameters that were used by me got saner names avilable from:
# * ParamAlias (misc parameters)
# * EnergyCalibration (params related to energy calibration)
# * SampleDescription (related to sample description)

invalid_par_patterns = {
    r'X_SSPDTIME\d*', 'X_NCLCOOLDATE', 'X_NCLCOOL2CLSC'
}

# for p in PARAM_GENERATOR.param_set():
#     if p.startswith("X"):
#         for pat in invalid_par_patterns:
#             if re.match(pat, p):
#                 continue
#         print(p)
#         param = PARAM_GENERATOR[p]
#         try:
#             value = params.get_parameter(conn, param)
#             print(value)
#             tm = convert_interval_to_absolute_date(value)
#             print(p, init.ffi.string(init.SAD_LIB.asctime(tm)))
#         except GenieError:
#             print(param)


# print(init.ffi.string(init.SAD_LIB.asctime(convert_interval_to_absolute_date(356*24*3600.0))))

dbl= params.get_parameter(conn, SampleDescription.MEASURE_START_TIME)

tmptr = convert_interval_to_absolute_date(dbl)

long_long = init.SAD_LIB.NotSadMkTime(tmptr)

print(time.localtime(long_long))
print(datetime.datetime.fromtimestamp(long_long))

# print(init.ffi.string(init.SAD_LIB.asctime(tmptr)))