#include <string.h>
#include "unity.h"
#include "customtype_mock.h"

#define MAX_LENGTH_ERROR_MESSAGE 100

static fooStruct fooData;
static barStruct barData;
static basStruct basData;

void customtype_MockSetup(void)
{
    memset(&fooData, 0, sizeof(fooData));
    memset(&barData, 0, sizeof(barData));
    memset(&basData, 0, sizeof(basData));
}

void customtype_MockTeardown(void)
{
    TEST_ASSERT_EQUAL_MESSAGE(fooData.ExpectedNrCalls,
                              fooData.CallCounter,
                              "foo was not called as often as specified!");
    TEST_ASSERT_EQUAL_MESSAGE(barData.ExpectedNrCalls,
                              barData.CallCounter,
                              "bar was not called as often as specified!");
    TEST_ASSERT_EQUAL_MESSAGE(basData.ExpectedNrCalls,
                              basData.CallCounter,
                              "bas was not called as often as specified!");
}


void foo_ExpectedCall(struct foo f, const struct foo *p1, const struct foo* p2, struct FOO ReturnValue)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(fooData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);
    TEST_ASSERT_NOT_NULL_MESSAGE(p1, "parameter should not be NULL");
    TEST_ASSERT_NOT_NULL_MESSAGE(p2, "parameter should not be NULL");

    fooData.f[fooData.ExpectedNrCalls] = f;
    fooData.p1[fooData.ExpectedNrCalls] = *p1;
    fooData.p2[fooData.ExpectedNrCalls] = *p2;
    fooData.ReturnValue[fooData.ExpectedNrCalls] = ReturnValue;
    fooData.ExpectedNrCalls++;
}

struct FOO foo(struct foo f, struct foo *p1, const struct foo* p2)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, fooData.ExpectedNrCalls, fooData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(fooData.CallCounter < fooData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, fooData.CallCounter+1);
    TEST_ASSERT_EQUAL_MEMORY_MESSAGE(&(fooData.f[fooData.CallCounter]), &f, sizeof(f), errormsg);
    *p1 = fooData.p1[fooData.CallCounter];
    TEST_ASSERT_EQUAL_MEMORY_MESSAGE(&(fooData.p2[fooData.CallCounter]), p2, sizeof(*p2), errormsg);
    return fooData.ReturnValue[fooData.CallCounter++];
}


void bar_ExpectedCall(const BAR* p1, const BAR *p2, BAR* ReturnValue)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(barData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);
    TEST_ASSERT_NOT_NULL_MESSAGE(p1, "parameter should not be NULL");
    TEST_ASSERT_NOT_NULL_MESSAGE(p2, "parameter should not be NULL");
    /* no TEST_ASSERT_NOT_NULL for ReturnValue, you might want to return NULL! */

    barData.p1[barData.ExpectedNrCalls] = *p1;
    barData.p2[barData.ExpectedNrCalls] = *p2;
    barData.ReturnValue[barData.ExpectedNrCalls] = ReturnValue;
    barData.ExpectedNrCalls++;
}

BAR* bar(BAR* p1, const BAR *p2)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, barData.ExpectedNrCalls, barData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(barData.CallCounter < barData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, barData.CallCounter+1);
    *p1 = barData.p1[barData.CallCounter];
    TEST_ASSERT_EQUAL_MEMORY_MESSAGE(&(barData.p2[barData.CallCounter]), p2, sizeof(*p2), errormsg);
    return barData.ReturnValue[barData.CallCounter++];
}


void bas_ExpectedCall(myInt i, const myInt* p, myInt ReturnValue)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(basData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);
    TEST_ASSERT_NOT_NULL_MESSAGE(p, "parameter should not be NULL");

    basData.i[basData.ExpectedNrCalls] = i;
    basData.p[basData.ExpectedNrCalls] = *p;
    basData.ReturnValue[basData.ExpectedNrCalls] = ReturnValue;
    basData.ExpectedNrCalls++;
}

myInt bas(myInt i, myInt* p)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, basData.ExpectedNrCalls, basData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(basData.CallCounter < basData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, basData.CallCounter+1);
    TEST_ASSERT_EQUAL_MEMORY_MESSAGE(&(basData.i[basData.CallCounter]), &i, sizeof(i), errormsg);
    *p = basData.p[basData.CallCounter];
    return basData.ReturnValue[basData.CallCounter++];
}
