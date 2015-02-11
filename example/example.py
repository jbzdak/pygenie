from uuid import uuid4
from pygenie import init
from pygenie.init import initialize; initialize() # Neccessary only if you want to overide path to S560 library

from pygenie.lib import create_vdm_connection, delete_vdm_connection, open_source, OpenFlags, SourceType, flush
from pygenie.lib import params
from pygenie.lib import spectrum

conn = create_vdm_connection()
# NativeSpect
# open_source(conn,  "C:\\GENIE2K\\CAMFILES\\NBSSTD.CNF", SourceType.NativeSpect, OpenFlags.ReadOnly)

open_source(conn,  "C:\\GENIE2K\\CAMFILES\\NAI2.CNF", SourceType.NativeSpect, OpenFlags.ReadOnly|OpenFlags.ReadWrite)

print(params.get_parameter(conn, params.ParamAlias.NUMBER_OF_CHANNELS))
print(params.get_parameter(conn, params.ParamAlias.TIME_LIVE))
print(params.get_parameter(conn, params.ParamAlias.TIME_REAL))
print(params.get_parameter(conn, params.EnergyCalibration.TYPE))
print(params.get_parameter(conn, params.PARAM_GENERATOR.T_STITLE))
print(params.get_parameter(conn, params.PARAM_GENERATOR.L_ECALTERMS))
print(params.get_parameter(conn, params.EnergyCalibration.POLYNOMIAL_N0))
print(params.get_parameter(conn, params.EnergyCalibration.POLYNOMIAL_N1))
print(params.get_parameter(conn, params.SampleDescription.DESCRIPTION[4]))

print("id {:x}".format(params.PARAM_GENERATOR.T_CTITLE.id))

print(spectrum.get_spectrum(conn, 0, 1024))
print(len(spectrum.get_spectrum(conn, 0, 1024)))

params.set_parameter(conn, params.SampleDescription.DESCRIPTION[4], str(uuid4()).encode("ascii"))

flush(conn)

# TODO: Call to flush needed?

delete_vdm_connection(conn)


