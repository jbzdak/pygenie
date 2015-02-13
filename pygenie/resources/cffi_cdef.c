
void vG2KEnv( void );
int iUtlCreateFileDSC2( HMEM  * phDSC, BOOL fAdvise, HWND hAdvise );
SADENTRY SadDeleteDSC( HMEM hDSC );
SADENTRY SadGetStatus( HMEM hDSC, ULONG * pulRC, short * psCli,
                                                 USHORT * pusAct );

SADENTRY SadOpenDataSource( HMEM hDSC, char * pszName,
                                 USHORT usType, short fsAccess,
                                 FLAG fVerify, char * pszShellID );

SADENTRY SadGetSpectrum( HMEM hDSC, USHORT usStart, USHORT usCount,
                                 FLAG fFloat, void * pvData );

SADENTRY SadGetParam( HMEM hDSC, ULONG ulParam,
                              USHORT usRecord,   USHORT usEntry,
                              void * pvData, USHORT usExpect );

SADENTRY SadPutParam( HMEM, ULONG, USHORT, USHORT, void *, USHORT );

BOOL fUtlCAMToCTime( double dTime, struct tm  * pstTime );

SADENTRY SadFlush( HMEM hDSC );

struct tm {
    int tm_sec;     /* seconds after the minute - [0,59] */
    int tm_min;     /* minutes after the hour - [0,59] */
    int tm_hour;    /* hours since midnight - [0,23] */
    int tm_mday;    /* day of the month - [1,31] */
    int tm_mon;     /* months since January - [0,11] */
    int tm_year;    /* years since 1900 */
    int tm_wday;    /* days since Sunday - [0,6] */
    int tm_yday;    /* days since January 1 - [0,365] */
    int tm_isdst;   /* daylight savings time flag */
};

long long NotSadMkTime(struct tm *timeptr);
