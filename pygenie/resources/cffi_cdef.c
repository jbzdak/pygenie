
void vG2KEnv( void );
int iUtlCreateFileDSC2( HMEM  * phDSC, BOOL fAdvise, HWND hAdvise );
SADENTRY SadDeleteDSC( HMEM hDSC );
SADENTRY SadGetStatus( HMEM hDSC, ULONG * pulRC, short * psCli,
                                                 USHORT * pusAct );

SADENTRY SadOpenDataSource( HMEM hDSC, char * pszName,
                                 USHORT usType, short fsAccess,
                                 FLAG fVerify, char * pszShellID );

#define VOID 0x1FF
//typedef char                CHAR;           /*  8 bit signed int            */

