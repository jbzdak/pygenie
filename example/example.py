
from pygenie.init import initialize

initialize() # Neccessary only if you want to overide path to S560 library

from pygenie.lib import create_vdm_connection, delete_vdm_connection, open_source, OpenFlags, SourceType


conn = create_vdm_connection()
# NativeSpect
open_source(conn,  "C:\\GENIE2K\\CAMFILES\\NBSSTD.CNF", SourceType.NativeSpect, OpenFlags.ReadOnly)

delete_vdm_connection(conn)


