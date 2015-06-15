#ifndef __FUNCPTR_MOCK_H
#define __FUNCPTR_MOCK_H

#include <stdbool.h>
#include <stdint.h>

#include "funcptr.h"

#define MAX_NR_FUNCTION_CALLS 25

typedef struct
{
    /* parameters */
    int time[MAX_NR_FUNCTION_CALLS];
    void (*callback[MAX_NR_FUNCTION_CALLS])(int id, char c, int(*foo)(bla i));
    int i[MAX_NR_FUNCTION_CALLS];
    /* return value */
    int ReturnValue[MAX_NR_FUNCTION_CALLS];
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} timerStruct;

typedef struct
{
    /* parameters */
    int time[MAX_NR_FUNCTION_CALLS];
    int **(*callback[MAX_NR_FUNCTION_CALLS])(int** p);
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} timerPointerStruct;

typedef struct
{
    /* parameters */
    int time[MAX_NR_FUNCTION_CALLS];
    int **(*callback[MAX_NR_FUNCTION_CALLS])(const int** p);
    /* administration */
    int CallCounter;
    int ExpectedNrCalls;
} timerConstPointerStruct;

void funcptr_MockSetup(void);    /* call this before every test! */
void funcptr_MockTeardown(void); /* call this after every test! */

/* call these for each call you expect for a given function */
void timer_ExpectedCall(int time, void (*callback)(int id, char c, int(*foo)(bla i)), int i, int ReturnValue); /* if you don't want to check function pointer(s), make it NULL */
void timerPointer_ExpectedCall(int time, int **(*callback)(int** p)); /* if you don't want to check function pointer(s), make it NULL */
void timerConstPointer_ExpectedCall(int time, int **(*callback)(const int** p)); /* if you don't want to check function pointer(s), make it NULL */

#endif  /* __FUNCPTR_MOCK_H */
