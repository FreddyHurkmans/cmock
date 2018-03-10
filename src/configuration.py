class Config(object):
    DESCRIPTION = 'Mock generator for c code'
    VERSION = '0.5'
    AUTHOR = 'Freddy Hurkmans'
    LICENSE = 'BSD 3-Clause'

    # set defaults for parameters
    verbose = False
    max_nr_function_calls = '25'
    charstar_is_input_string = False

    UNITY_INCLUDE = '#include "unity.h"'
    # CUSTOM_INCLUDES = ['#include "resource_detector.h"']
    CUSTOM_INCLUDES = []

    # List of all supported c types and the matching unity ASSERT macro's
    # If these types have different sizes on your system, you can simply
    # correct the macros. If you have missing types, you can simply add
    # your type/macro pairs
    CTYPE_TO_UNITY_ASSERT_MACRO = [
        ['char', 'TEST_ASSERT_EQUAL_INT8_MESSAGE'],
        ['signed char', 'TEST_ASSERT_EQUAL_INT8_MESSAGE'],
        ['unsigned char', 'TEST_ASSERT_EQUAL_UINT8_MESSAGE'],
        ['short', 'TEST_ASSERT_EQUAL_INT16_MESSAGE'],
        ['short int', 'TEST_ASSERT_EQUAL_INT16_MESSAGE'],
        ['signed short', 'TEST_ASSERT_EQUAL_INT16_MESSAGE'],
        ['signed short int', 'TEST_ASSERT_EQUAL_INT16_MESSAGE'],
        ['unsigned short', 'TEST_ASSERT_EQUAL_UINT16_MESSAGE'],
        ['unsigned short int', 'TEST_ASSERT_EQUAL_UINT16_MESSAGE'],
        ['int', 'TEST_ASSERT_EQUAL_INT_MESSAGE'],
        ['signed int', 'TEST_ASSERT_EQUAL_INT_MESSAGE'],
        ['unsigned', 'TEST_ASSERT_EQUAL_UINT_MESSAGE'],
        ['unsigned int', 'TEST_ASSERT_EQUAL_UINT_MESSAGE'],
        ['long', 'TEST_ASSERT_EQUAL_INT64_MESSAGE'],
        ['long int', 'TEST_ASSERT_EQUAL_INT64_MESSAGE'],
        ['signed long', 'TEST_ASSERT_EQUAL_INT64_MESSAGE'],
        ['signed long int', 'TEST_ASSERT_EQUAL_INT64_MESSAGE'],
        ['unsigned long', 'TEST_ASSERT_EQUAL_UINT64_MESSAGE'],
        ['unsigned long int', 'TEST_ASSERT_EQUAL_UINT64_MESSAGE'],
        ['float', 'TEST_ASSERT_EQUAL_FLOAT_MESSAGE'],
        ['double', 'TEST_ASSERT_EQUAL_FLOAT_MESSAGE'],
        ['long double', 'TEST_ASSERT_EQUAL_FLOAT_MESSAGE'],
        ['int8_t', 'TEST_ASSERT_EQUAL_INT8_MESSAGE'],
        ['int16_t', 'TEST_ASSERT_EQUAL_INT16_MESSAGE'],
        ['int32_t', 'TEST_ASSERT_EQUAL_INT32_MESSAGE'],
        ['int64_t', 'TEST_ASSERT_EQUAL_INT64_MESSAGE'],
        ['uint8_t', 'TEST_ASSERT_EQUAL_UINT8_MESSAGE'],
        ['uint16_t', 'TEST_ASSERT_EQUAL_UINT16_MESSAGE'],
        ['uint32_t', 'TEST_ASSERT_EQUAL_UINT32_MESSAGE'],
        ['uint64_t', 'TEST_ASSERT_EQUAL_UINT64_MESSAGE']
    ]

    CTAGS_EXECUTABLE = 'ctags'
