

from pygenie import init
from pygenie.init import initialize

initialize() # Neccessary only if you want to overide path to S560 library

from pygenie.lib import create_vdm_connection, delete_vdm_connection, open_source, OpenFlags, SourceType
from pygenie.lib import params
from pygenie.lib import spectrum

conn = create_vdm_connection()
# NativeSpect
# open_source(conn,  "C:\\GENIE2K\\CAMFILES\\NBSSTD.CNF", SourceType.NativeSpect, OpenFlags.ReadOnly)

open_source(conn,  "C:\\GENIE2K\\CAMFILES\\Cernipf.CNF", SourceType.NativeSpect, OpenFlags.ReadOnly)

print(params.get_parameter(conn, params.ParamAlias.NUMBER_OF_CHANNELS))
print(params.get_parameter(conn, params.ParamAlias.TIME_LIVE))
print(params.get_parameter(conn, params.ParamAlias.TIME_REAL))
print(params.get_parameter(conn, params.EnergyCalibration.TYPE))
print(params.get_parameter(conn, params.PARAM_GENERATOR.T_STITLE))
print(params.get_parameter(conn, params.PARAM_GENERATOR.L_ECALTERMS))
print(params.get_parameter(conn, params.EnergyCalibration.POLYNOMIAL_N0))
print(params.get_parameter(conn, params.EnergyCalibration.POLYNOMIAL_N1))

print("id {:x}".format(params.PARAM_GENERATOR.T_CTITLE.id))

print(spectrum.get_spectrum(conn, 0, 4096))
print(len(spectrum.get_spectrum(conn, 0, 4096)))

# print(spectrum._get_spectrum_simple(conn, 0, 200))

# print(len(spectrum._get_spectrum_simple(conn, 0, 200)))

# data = init.ffi.new("char[]", 17)
# init.SAD_LIB.SadGetParam(conn,
#     0X20010003,
#     1, 1, data, 17)
#
# print(init.ffi.string(data))

# print(b"".join([data[ii] for ii in range(17)]))


delete_vdm_connection(conn)


