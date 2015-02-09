#include <windows.h>
#include <crackers.h>
#include <tchar.h>
#include <stdio.h>
#include <citypes.h>
#include <spasst.h>
#include <sad.h>
#include <ci_files.h>
#include <campdef.h>
#include <cam_n.h>
#include <utility.h>

#include <stdio.h>
#include <string.h>

#include <stdlib.h>

struct char_param{
    short error;
    char* param_value;
} ;


struct char_param NotSoSadGetCharParam(HMEM hDSC, ULONG ulParam,
                              USHORT usRecord,   USHORT usEntry, USHORT usExpect){
	int ii = 0;

    char* data = memset(malloc(usExpect), '\0', usExpect);

	short error = SadGetParam(hDSC, ulParam, usRecord, usEntry,  &data, usExpect);

    struct char_param result = {error, (char*)data};

    printf("Foo bar baz");


    for(ii=0; ii<usExpect; ii++){
        putchar(data[ii]);
    }
    //printf("Foo bar baz");
    return result;
}

