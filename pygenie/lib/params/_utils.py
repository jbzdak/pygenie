
import datetime

from pygenie import init
from pygenie.lib.errors import GenieDatetimeConversionError

def convert_interval_to_absolute_date(interval):
    tm = init.ffi.new("struct tm[1]")
    result = init.SAD_LIB.fUtlCAMToCTime(interval, tm)
    if result != 0:
        raise GenieDatetimeConversionError("Error converting float {} to tm structure".format(interval))
    sane_time_since_epoch = init.SAD_LIB.NotSadMkTime(tm)
    return datetime.datetime.fromtimestamp(sane_time_since_epoch)


