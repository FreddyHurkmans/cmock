#ifndef __SIMPLE_MOCK_H
#define __SIMPLE_MOCK_H

#include <stdbool.h>
#include <stdint.h>

#include "simple.h"

#define MAX_NR_FUNCTION_CALLS 25

typedef struct
{
    /* return value */
    double ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} piStruct;

typedef struct
{
    /* parameters */
    int nr[MAX_NR_FUNCTION_CALLS];
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} fooStruct;

typedef struct
{
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} barStruct;

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
} basStruct;

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
} constPtrsStruct;

void simple_MockSetup(void);    /* call this before every test! */
void simple_MockTeardown(void); /* call this after every test! */

/* call these for each call you expect for a given function */
void pi_ExpectedCall(double ReturnValue);
void foo_ExpectedCall(int nr, int ReturnValue);
void bar_ExpectedCall(int ReturnValue);
void bas_ExpectedCall(uint8_t v1, int16_t v2, const int32_t* p1, uint_16_t ReturnValue);
void constPtrs_ExpectedCall(const int* p1, const int *p2, int const* p3, int const *p4, int ReturnValue);

#endif  /* __SIMPLE_MOCK_H */
