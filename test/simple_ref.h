#ifndef SIMPLE_MOCK_H
#define SIMPLE_MOCK_H

#include "simple.h"

#include <stdbool.h>
#include <stdint.h>

#define MAX_NR_FUNCTION_CALLS 25

typedef struct
{
    /* return value */
    double ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} piMockData;

typedef struct
{
    /* parameters */
    int nr[MAX_NR_FUNCTION_CALLS];
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} fooMockData;

typedef struct
{
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} barMockData;

typedef struct
{
    /* parameters */
    uint8_t v1[MAX_NR_FUNCTION_CALLS];
    int16_t v2[MAX_NR_FUNCTION_CALLS];
    int32_t p1[MAX_NR_FUNCTION_CALLS];
    /* return value */
    uint_16_t ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} basMockData;

typedef struct
{
    /* parameters */
    int p1[MAX_NR_FUNCTION_CALLS];
    int p2[MAX_NR_FUNCTION_CALLS];
    int p3[MAX_NR_FUNCTION_CALLS];
    int p4[MAX_NR_FUNCTION_CALLS];
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} constPtrsMockData;

void simple_MockSetup(void);    /* call this from the Setup of your test! */
void simple_MockTeardown(void); /* call this from the Teardown of your test! */

/* call these for each call you expect for a given function */
void pi_ExpectedCall(double ReturnValue);
void foo_ExpectedCall(int nr, int ReturnValue);
void bar_ExpectedCall(int ReturnValue);
void bas_ExpectedCall(uint8_t v1, int16_t v2, const int32_t* p1, uint_16_t ReturnValue);
void constPtrs_ExpectedCall(const int* p1, const int *p2, int const* p3, int const *p4, int ReturnValue);

#endif  /* SIMPLE_MOCK_H */
