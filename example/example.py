
from pygenie.init import initialize

initialize() # Neccessary only if you want to overide path to S560 library

from pygenie.lib import create_vdm_connection, delete_vdm_connection, open_source, OpenFlags, SourceType
from pygenie.lib import params

conn = create_vdm_connection()
# NativeSpect
open_source(conn,  "C:\\GENIE2K\\CAMFILES\\NBSSTD.CNF", SourceType.NativeSpect, OpenFlags.ReadOnly)

print(params.get_parameter(conn, params.ParamAlias.NUMBER_OF_CHANNELS))

delete_vdm_connection(conn)


