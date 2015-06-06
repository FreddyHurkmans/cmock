#include <string.h>
#include <stdlib.h>
#include "unity.h"
#include "simple_mock.h"

#define MAX_LENGTH_ERROR_MESSAGE 100

static piStruct piData;
static fooStruct fooData;
static barStruct barData;
static basStruct basData;
static constPtrsStruct constPtrsData;

void simple_MockSetup(void)
{
    memset(&piData, 0, sizeof(piData));
    memset(&fooData, 0, sizeof(fooData));
    memset(&barData, 0, sizeof(barData));
    memset(&basData, 0, sizeof(basData));
    memset(&constPtrsData, 0, sizeof(constPtrsData));
}

void simple_MockTeardown(void)
{
    TEST_ASSERT_EQUAL_MESSAGE(piData.ExpectedNrCalls,
                              piData.CallCounter,
                              "pi was not called as often as specified!");
    TEST_ASSERT_EQUAL_MESSAGE(fooData.ExpectedNrCalls,
                              fooData.CallCounter,
                              "foo was not called as often as specified!");
    TEST_ASSERT_EQUAL_MESSAGE(barData.ExpectedNrCalls,
                              barData.CallCounter,
                              "bar was not called as often as specified!");
    TEST_ASSERT_EQUAL_MESSAGE(basData.ExpectedNrCalls,
                              basData.CallCounter,
                              "bas was not called as often as specified!");
    TEST_ASSERT_EQUAL_MESSAGE(constPtrsData.ExpectedNrCalls,
                              constPtrsData.CallCounter,
                              "constPtrs was not called as often as specified!");
}


void pi_ExpectedCall(double ReturnValue)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(piData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);

    piData.ReturnValue[piData.ExpectedNrCalls] = ReturnValue;
    piData.ExpectedNrCalls++;
}

double pi(void)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, piData.ExpectedNrCalls, piData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(piData.CallCounter < piData.ExpectedNrCalls, errormsg);

    return piData.ReturnValue[piData.CallCounter++];
}


void foo_ExpectedCall(int nr, int ReturnValue)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(fooData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);

    fooData.nr[fooData.ExpectedNrCalls] = nr;
    fooData.ReturnValue[fooData.ExpectedNrCalls] = ReturnValue;
    fooData.ExpectedNrCalls++;
}

int foo(int nr)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, fooData.ExpectedNrCalls, fooData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(fooData.CallCounter < fooData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, fooData.CallCounter+1);
    TEST_ASSERT_EQUAL_INT_MESSAGE(fooData.nr[fooData.CallCounter], nr, errormsg);
    return fooData.ReturnValue[fooData.CallCounter++];
}


void bar_ExpectedCall(int ReturnValue)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(barData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);

    barData.ReturnValue[barData.ExpectedNrCalls] = ReturnValue;
    barData.ExpectedNrCalls++;
}

int bar(void)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, barData.ExpectedNrCalls, barData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(barData.CallCounter < barData.ExpectedNrCalls, errormsg);

    return barData.ReturnValue[barData.CallCounter++];
}


void bas_ExpectedCall(uint8_t v1, int16_t v2, const int32_t* p1, uint_16_t ReturnValue)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(basData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);
    TEST_ASSERT_NOT_NULL_MESSAGE(p1, "parameter should not be NULL");

    basData.v1[basData.ExpectedNrCalls] = v1;
    basData.v2[basData.ExpectedNrCalls] = v2;
    basData.p1[basData.ExpectedNrCalls] = *p1;
    basData.ReturnValue[basData.ExpectedNrCalls] = ReturnValue;
    basData.ExpectedNrCalls++;
}

uint_16_t bas(uint8_t v1, int16_t v2, int32_t* p1)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, basData.ExpectedNrCalls, basData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(basData.CallCounter < basData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, basData.CallCounter+1);
    TEST_ASSERT_EQUAL_UINT8_MESSAGE(basData.v1[basData.CallCounter], v1, errormsg);
    TEST_ASSERT_EQUAL_INT16_MESSAGE(basData.v2[basData.CallCounter], v2, errormsg);
    *p1 = basData.p1[basData.CallCounter];
    return basData.ReturnValue[basData.CallCounter++];
}


void constPtrs_ExpectedCall(const int* p1, const int *p2, int const* p3, int const *p4, int ReturnValue)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(constPtrsData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);
    TEST_ASSERT_NOT_NULL_MESSAGE(p1, "parameter should not be NULL");
    TEST_ASSERT_NOT_NULL_MESSAGE(p2, "parameter should not be NULL");
    TEST_ASSERT_NOT_NULL_MESSAGE(p3, "parameter should not be NULL");
    TEST_ASSERT_NOT_NULL_MESSAGE(p4, "parameter should not be NULL");

    constPtrsData.p1[constPtrsData.ExpectedNrCalls] = *p1;
    constPtrsData.p2[constPtrsData.ExpectedNrCalls] = *p2;
    constPtrsData.p3[constPtrsData.ExpectedNrCalls] = *p3;
    constPtrsData.p4[constPtrsData.ExpectedNrCalls] = *p4;
    constPtrsData.ReturnValue[constPtrsData.ExpectedNrCalls] = ReturnValue;
    constPtrsData.ExpectedNrCalls++;
}

int constPtrs(const int* p1, const int *p2, int const* p3, int const *p4)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, constPtrsData.ExpectedNrCalls, constPtrsData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(constPtrsData.CallCounter < constPtrsData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, constPtrsData.CallCounter+1);
    TEST_ASSERT_EQUAL_INT_MESSAGE(constPtrsData.p1[constPtrsData.CallCounter], *p1, errormsg);
    TEST_ASSERT_EQUAL_INT_MESSAGE(constPtrsData.p2[constPtrsData.CallCounter], *p2, errormsg);
    TEST_ASSERT_EQUAL_INT_MESSAGE(constPtrsData.p3[constPtrsData.CallCounter], *p3, errormsg);
    TEST_ASSERT_EQUAL_INT_MESSAGE(constPtrsData.p4[constPtrsData.CallCounter], *p4, errormsg);
    return constPtrsData.ReturnValue[constPtrsData.CallCounter++];
}
