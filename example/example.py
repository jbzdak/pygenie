from uuid import uuid4

import numpy as np

from pygenie.init import initialize; initialize() # Neccessary only if you want to overide path to S560 library

from pygenie.lib import create_vdm_connection, delete_vdm_connection, open_source, OpenFlags, SourceType, flush
from pygenie.lib import params
from pygenie.lib import spectrum

import datetime

conn = create_vdm_connection()

open_source(conn,  "C:\\GENIE2K\\CAMFILES\\NAI2.CNF", SourceType.NativeSpect, OpenFlags.ReadOnly|OpenFlags.ReadWrite)

# Parameter reading is easy, but there are many ways to obtain parameter object
# All defined parameters are avilable from PARAM_GENERATOR object
# Parameters that were used by me got saner names avilable from:
# * ParamAlias (misc parameters)
# * EnergyCalibration (params related to energy calibration)
# * SampleDescription (related to sample description)

print(params.get_parameter(conn, params.ParamAlias.NUMBER_OF_CHANNELS))
print(params.get_parameter(conn, params.ParamAlias.TIME_LIVE))
print(params.get_parameter(conn, params.ParamAlias.TIME_REAL))
print(params.get_parameter(conn, params.EnergyCalibration.TYPE))
print(params.get_parameter(conn, params.PARAM_GENERATOR.T_STITLE))
print(params.get_parameter(conn, params.PARAM_GENERATOR.L_ECALTERMS))
print(params.get_parameter(conn, params.SampleDescription.DESCRIPTION[4]))

print(params.get_parameter(conn, params.SampleDescription.MEASURE_START_TIME))

# This gets calibration as numpy polynomial

# 10-09- 2014
# print("DATETIME " + datetime.datetime(1970, 1, 1,) + datetime.timedelta(seconds=params.get_calibration(conn)))

tm = params.get_parameter(conn, params.SampleDescription.MEASURE_START_TIME)

print(tm.tm_year)
print(tm.tm_mon)
print(tm.tm_mday)

print("id {:x}".format(params.PARAM_GENERATOR.T_CTITLE.id))

poly = params.get_calibration(conn)

# This calculates energy for each channel
print(np.polyval(poly, np.arange(1, 1024)))

# Prints spectrum:
print(spectrum.get_spectrum(conn, 0, 1024))
print(len(spectrum.get_spectrum(conn, 0, 1024)))

# Sets parameter:
params.set_parameter(conn, params.SampleDescription.DESCRIPTION[4], str(uuid4()).encode("ascii"))

# Remember to flush it
flush(conn)

delete_vdm_connection(conn)


