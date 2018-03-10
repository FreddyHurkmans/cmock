#include "string2_mock.h"
#include "unity.h"
#include <string.h>
#include <stdlib.h>

#define MAX_LENGTH_ERROR_MESSAGE 100

static sendMockData sendData;

void string2_MockSetup(void)
{
    memset(&sendData, 0, sizeof(sendData));
}

void string2_MockTeardown(void)
{
    TEST_ASSERT_EQUAL_MESSAGE(sendData.ExpectedNrCalls,
                              sendData.CallCounter,
                              "send was not called as often as specified!");
}


void send_ExpectedCall(const char* text, int ReturnValue)
{
    size_t length = 0;
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(sendData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);
    TEST_ASSERT_NOT_NULL_MESSAGE(text, "parameter should not be NULL");

    length = strlen(text);
    sendData.text[sendData.ExpectedNrCalls] = malloc(length+1);
    TEST_ASSERT_NOT_NULL_MESSAGE(sendData.text[sendData.ExpectedNrCalls], "could not allocate memory");
    strcpy(sendData.text[sendData.ExpectedNrCalls], text);
    sendData.ReturnValue[sendData.ExpectedNrCalls] = ReturnValue;
    sendData.ExpectedNrCalls++;
}

int send(char* text)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, sendData.ExpectedNrCalls, sendData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(sendData.CallCounter < sendData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, sendData.CallCounter+1);
    TEST_ASSERT_EQUAL_STRING_MESSAGE(sendData.text[sendData.CallCounter], text, errormsg);
    free(sendData.text[sendData.CallCounter]);
    sendData.text[sendData.CallCounter] = NULL;
    return sendData.ReturnValue[sendData.CallCounter++];
}
