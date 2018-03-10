#ifndef STRING2_MOCK_H
#define STRING2_MOCK_H

#include "string2.h"

#include <stdbool.h>
#include <stdint.h>

#define MAX_NR_FUNCTION_CALLS 25

typedef struct
{
    /* parameters */
    char* text[MAX_NR_FUNCTION_CALLS];
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} sendMockData;

void string2_MockSetup(void);    /* call this from the Setup of your test! */
void string2_MockTeardown(void); /* call this from the Teardown of your test! */

/* call these for each call you expect for a given function */
void send_ExpectedCall(const char* text, int ReturnValue);

#endif  /* STRING2_MOCK_H */
