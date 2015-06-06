#ifndef __CUSTOMTYPE_MOCK_H
#define __CUSTOMTYPE_MOCK_H

#include <stdbool.h>
#include <stdint.h>

#include "customtype.h"

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
} fooStruct;

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
} barStruct;

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
} basStruct;

void customtype_MockSetup(void);    /* call this before every test! */
void customtype_MockTeardown(void); /* call this after every test! */

/* call these for each call you expect for a given function */
void foo_ExpectedCall(struct foo f, const struct foo *p1, const struct foo* p2, struct FOO ReturnValue);
void bar_ExpectedCall(const BAR* p1, const BAR *p2, BAR* ReturnValue);
void bas_ExpectedCall(myInt i, const myInt* p, myInt ReturnValue);

#endif  /* __CUSTOMTYPE_MOCK_H */
