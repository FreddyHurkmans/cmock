#ifndef FUNCPTR_MOCK_H
#define FUNCPTR_MOCK_H

#include "funcptr.h"

#include <stdbool.h>
#include <stdint.h>

#define MAX_NR_FUNCTION_CALLS 25

typedef struct
{
    /* parameters */
    int time[MAX_NR_FUNCTION_CALLS];
    void (*callback[MAX_NR_FUNCTION_CALLS])(int id, char c, int(*foo)(bla i));
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} timerMockData;

typedef struct
{
    /* parameters */
    int time[MAX_NR_FUNCTION_CALLS];
    int **(*callback[MAX_NR_FUNCTION_CALLS])(int** p);
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} timerPointerMockData;

typedef struct
{
    /* parameters */
    int time[MAX_NR_FUNCTION_CALLS];
    int **(*callback[MAX_NR_FUNCTION_CALLS])(const int** p);
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} timerConstPointerMockData;

void funcptr_MockSetup(void);    /* call this from the Setup of your test! */
void funcptr_MockTeardown(void); /* call this from the Teardown of your test! */

/* call these for each call you expect for a given function */
void timer_ExpectedCall(int time, void (*callback)(int id, char c, int(*foo)(bla i)), int ReturnValue); /* if you don't want to check function pointer(s), make it NULL */
void timerPointer_ExpectedCall(int time, int **(*callback)(int** p)); /* if you don't want to check function pointer(s), make it NULL */
void timerConstPointer_ExpectedCall(int time, int **(*callback)(const int** p)); /* if you don't want to check function pointer(s), make it NULL */

#endif  /* FUNCPTR_MOCK_H */
