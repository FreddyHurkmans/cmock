#include "funcptr_mock.h"
#include "unity.h"
#include <string.h>
#include <stdlib.h>

#define MAX_LENGTH_ERROR_MESSAGE 100

static timerMockData timerData;
static timerPointerMockData timerPointerData;
static timerConstPointerMockData timerConstPointerData;

void funcptr_MockSetup(void)
{
    memset(&timerData, 0, sizeof(timerData));
    memset(&timerPointerData, 0, sizeof(timerPointerData));
    memset(&timerConstPointerData, 0, sizeof(timerConstPointerData));
}

void funcptr_MockTeardown(void)
{
    TEST_ASSERT_EQUAL_MESSAGE(timerData.ExpectedNrCalls,
                              timerData.CallCounter,
                              "timer was not called as often as specified!");
    TEST_ASSERT_EQUAL_MESSAGE(timerPointerData.ExpectedNrCalls,
                              timerPointerData.CallCounter,
                              "timerPointer was not called as often as specified!");
    TEST_ASSERT_EQUAL_MESSAGE(timerConstPointerData.ExpectedNrCalls,
                              timerConstPointerData.CallCounter,
                              "timerConstPointer was not called as often as specified!");
}


void timer_ExpectedCall(int time, void (*callback)(int id, char c, int(*foo)(bla i)), int ReturnValue) /* if you don't want to check function pointer(s), make it NULL */
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(timerData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);

    timerData.time[timerData.ExpectedNrCalls] = time;
    timerData.callback[timerData.ExpectedNrCalls] = callback;
    timerData.ReturnValue[timerData.ExpectedNrCalls] = ReturnValue;
    timerData.ExpectedNrCalls++;
}

int timer(int time, void (*callback)(int id, char c, int(*foo)(bla i)))
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, timerData.ExpectedNrCalls, timerData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(timerData.CallCounter < timerData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, timerData.CallCounter+1);
    TEST_ASSERT_EQUAL_INT_MESSAGE(timerData.time[timerData.CallCounter], time, errormsg);
    if (callback != NULL) TEST_ASSERT_EQUAL_PTR_MESSAGE(timerData.callback[timerData.CallCounter], callback, errormsg);
    return timerData.ReturnValue[timerData.CallCounter++];
}


void timerPointer_ExpectedCall(int time, int **(*callback)(int** p)) /* if you don't want to check function pointer(s), make it NULL */
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(timerPointerData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);

    timerPointerData.time[timerPointerData.ExpectedNrCalls] = time;
    timerPointerData.callback[timerPointerData.ExpectedNrCalls] = callback;
    timerPointerData.ExpectedNrCalls++;
}

void timerPointer(int time, int **(*callback)(int** p))
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, timerPointerData.ExpectedNrCalls, timerPointerData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(timerPointerData.CallCounter < timerPointerData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, timerPointerData.CallCounter+1);
    TEST_ASSERT_EQUAL_INT_MESSAGE(timerPointerData.time[timerPointerData.CallCounter], time, errormsg);
    if (callback != NULL) TEST_ASSERT_EQUAL_PTR_MESSAGE(timerPointerData.callback[timerPointerData.CallCounter], callback, errormsg);
    timerPointerData.CallCounter++;
}


void timerConstPointer_ExpectedCall(int time, int **(*callback)(const int** p)) /* if you don't want to check function pointer(s), make it NULL */
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(timerConstPointerData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);

    timerConstPointerData.time[timerConstPointerData.ExpectedNrCalls] = time;
    timerConstPointerData.callback[timerConstPointerData.ExpectedNrCalls] = callback;
    timerConstPointerData.ExpectedNrCalls++;
}

void timerConstPointer(int time, int **(*callback)(const int** p))
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, timerConstPointerData.ExpectedNrCalls, timerConstPointerData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(timerConstPointerData.CallCounter < timerConstPointerData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, timerConstPointerData.CallCounter+1);
    TEST_ASSERT_EQUAL_INT_MESSAGE(timerConstPointerData.time[timerConstPointerData.CallCounter], time, errormsg);
    if (callback != NULL) TEST_ASSERT_EQUAL_PTR_MESSAGE(timerConstPointerData.callback[timerConstPointerData.CallCounter], callback, errormsg);
    timerConstPointerData.CallCounter++;
}
