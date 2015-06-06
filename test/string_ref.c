#include <string.h>
#include <stdlib.h>
#include "unity.h"
#include "string_mock.h"

#define MAX_LENGTH_ERROR_MESSAGE 100

static fakeSendStruct fakeSendData;
static sendStruct sendData;
static recvStruct recvData;

void string_MockSetup(void)
{
    memset(&fakeSendData, 0, sizeof(fakeSendData));
    memset(&sendData, 0, sizeof(sendData));
    memset(&recvData, 0, sizeof(recvData));
}

void string_MockTeardown(void)
{
    TEST_ASSERT_EQUAL_MESSAGE(fakeSendData.ExpectedNrCalls,
                              fakeSendData.CallCounter,
                              "fakeSend was not called as often as specified!");
    TEST_ASSERT_EQUAL_MESSAGE(sendData.ExpectedNrCalls,
                              sendData.CallCounter,
                              "send was not called as often as specified!");
    TEST_ASSERT_EQUAL_MESSAGE(recvData.ExpectedNrCalls,
                              recvData.CallCounter,
                              "recv was not called as often as specified!");
}


void fakeSend_ExpectedCall(const unsigned char* character, int ReturnValue)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(fakeSendData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);
    TEST_ASSERT_NOT_NULL_MESSAGE(character, "parameter should not be NULL");

    fakeSendData.character[fakeSendData.ExpectedNrCalls] = *character;
    fakeSendData.ReturnValue[fakeSendData.ExpectedNrCalls] = ReturnValue;
    fakeSendData.ExpectedNrCalls++;
}

int fakeSend(unsigned char* character)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, fakeSendData.ExpectedNrCalls, fakeSendData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(fakeSendData.CallCounter < fakeSendData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, fakeSendData.CallCounter+1);
    *character = fakeSendData.character[fakeSendData.CallCounter];
    return fakeSendData.ReturnValue[fakeSendData.CallCounter++];
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

int send(const char* text)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, sendData.ExpectedNrCalls, sendData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(sendData.CallCounter < sendData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, sendData.CallCounter+1);
    TEST_ASSERT_EQUAL_STRING_MESSAGE(sendData.text[sendData.CallCounter], text, errormsg);
    free(sendData.text[sendData.CallCounter]);
    return sendData.ReturnValue[sendData.CallCounter++];
}


void recv_ExpectedCall(const char* character, int ReturnValue)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];
    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);
    TEST_ASSERT_TRUE_MESSAGE(recvData.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);
    TEST_ASSERT_NOT_NULL_MESSAGE(character, "parameter should not be NULL");

    recvData.character[recvData.ExpectedNrCalls] = *character;
    recvData.ReturnValue[recvData.ExpectedNrCalls] = ReturnValue;
    recvData.ExpectedNrCalls++;
}

int recv(char* character)
{
    char errormsg[MAX_LENGTH_ERROR_MESSAGE];

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, recvData.ExpectedNrCalls, recvData.CallCounter+1);
    TEST_ASSERT_TRUE_MESSAGE(recvData.CallCounter < recvData.ExpectedNrCalls, errormsg);

    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, recvData.CallCounter+1);
    *character = recvData.character[recvData.CallCounter];
    return recvData.ReturnValue[recvData.CallCounter++];
}
