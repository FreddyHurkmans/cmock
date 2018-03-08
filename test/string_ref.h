#ifndef STRING_MOCK_H
#define STRING_MOCK_H

#include "string.h"

#include <stdbool.h>
#include <stdint.h>

#define MAX_NR_FUNCTION_CALLS 25

typedef struct
{
    /* parameters */
    unsigned char character[MAX_NR_FUNCTION_CALLS];
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} fakeSendMockData;

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

typedef struct
{
    /* parameters */
    char character[MAX_NR_FUNCTION_CALLS];
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} recvMockData;

void string_MockSetup(void);    /* call this from the Setup of your test! */
void string_MockTeardown(void); /* call this from the Teardown of your test! */

/* call these for each call you expect for a given function */
void fakeSend_ExpectedCall(const unsigned char* character, int ReturnValue);
void send_ExpectedCall(const char* text, int ReturnValue);
void recv_ExpectedCall(const char* character, int ReturnValue);

#endif  /* STRING_MOCK_H */
