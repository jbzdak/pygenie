

from pygenie import init
from pygenie.init import initialize

initialize() # Neccessary only if you want to overide path to S560 library

from pygenie.lib import create_vdm_connection, delete_vdm_connection, open_source, OpenFlags, SourceType
from pygenie.lib import params

conn = create_vdm_connection()
# NativeSpect
open_source(conn,  "C:\\GENIE2K\\CAMFILES\\NBSSTD.CNF", SourceType.NativeSpect, OpenFlags.ReadOnly)

print(params.get_parameter(conn, params.ParamAlias.NUMBER_OF_CHANNELS))
print(params.get_parameter(conn, params.ParamAlias.TIME_LIVE))
print(params.get_parameter(conn, params.ParamAlias.TIME_REAL))
print(params.get_parameter(conn, params.ParamAlias.ENERGY_CALIBRATION_TYPE))
print(params.get_parameter(conn, params.PARAM_GENERATOR.T_CTITLE))

print("id {:x}".format(params.PARAM_GENERATOR.T_CTITLE.id))

# data = init.ffi.new("char[]", 17)
# init.SAD_LIB.SadGetParam(conn,
#     0X20010003,
#     1, 1, data, 17)
#
# print(init.ffi.string(data))

# print(b"".join([data[ii] for ii in range(17)]))


delete_vdm_connection(conn)


