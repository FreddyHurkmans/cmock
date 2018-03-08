#ifndef CUSTOMTYPE_MOCK_H
#define CUSTOMTYPE_MOCK_H

#include "customtype.h"

#include <stdbool.h>
#include <stdint.h>

#define MAX_NR_FUNCTION_CALLS 25

typedef struct
{
    /* parameters */
    struct foo f[MAX_NR_FUNCTION_CALLS];
    struct foo p1[MAX_NR_FUNCTION_CALLS];
    struct foo p2[MAX_NR_FUNCTION_CALLS];
    /* return value */
    struct FOO ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} fooMockData;

typedef struct
{
    /* parameters */
    BAR p1[MAX_NR_FUNCTION_CALLS];
    BAR p2[MAX_NR_FUNCTION_CALLS];
    /* return value */
    BAR* ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} barMockData;

typedef struct
{
    /* parameters */
    myInt i[MAX_NR_FUNCTION_CALLS];
    myInt p[MAX_NR_FUNCTION_CALLS];
    /* return value */
    myInt ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} basMockData;

void customtype_MockSetup(void);    /* call this from the Setup of your test! */
void customtype_MockTeardown(void); /* call this from the Teardown of your test! */

/* call these for each call you expect for a given function */
void foo_ExpectedCall(struct foo f, const struct foo *p1, const struct foo* p2, struct FOO ReturnValue);
void bar_ExpectedCall(const BAR* p1, const BAR *p2, BAR* ReturnValue);
void bas_ExpectedCall(myInt i, const myInt* p, myInt ReturnValue);

#endif  /* CUSTOMTYPE_MOCK_H */
