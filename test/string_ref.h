#ifndef __STRING_MOCK_H
#define __STRING_MOCK_H

#include <stdbool.h>
#include <stdint.h>

#include "string.h"

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
} fakeSendStruct;

typedef struct
{
    /* parameters */
    char* text[MAX_NR_FUNCTION_CALLS];
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} sendStruct;

typedef struct
{
    /* parameters */
    char character[MAX_NR_FUNCTION_CALLS];
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} recvStruct;

void string_MockSetup(void);    /* call this before every test! */
void string_MockTeardown(void); /* call this after every test! */

/* call these for each call you expect for a given function */
void fakeSend_ExpectedCall(const unsigned char* character, int ReturnValue);
void send_ExpectedCall(const char* text, int ReturnValue);
void recv_ExpectedCall(const char* character, int ReturnValue);

#endif  /* __STRING_MOCK_H */
