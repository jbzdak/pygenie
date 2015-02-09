
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

//#define VOID 0x1FF
//typedef char                CHAR;           /*  8 bit signed int            */

struct char_param{
    short error;
    char* param_value;
} ;

struct char_param NotSoSadGetCharParam(HMEM hDSC, ULONG ulParam,
                              USHORT usRecord,   USHORT usEntry, USHORT usExpect);