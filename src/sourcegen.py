from cfile_writer import *
from protogen import *
from configuration import *


class SourceGenerator(object):
    def __init__(self, input_header, max_nr_function_calls, version):
        self.__max_nr_function_calls = max_nr_function_calls
        self.__proto = PrototypeGenerator()
        self.__file = CFileWriter(input_header, '.c', version)

    def generate(self, mockinfo):
        self.__write_includes_to_sourcefile()
        self.__write_defines_to_sourcefile()
        self.__write_global_vars_to_sourcefile(mockinfo)
        self.__write_setup_and_teardown_to_sourcefile(mockinfo)
        for mock in mockinfo:
            self.__write_expected_call_function(mock)
            self.__write_mock_function(mock)

    def __write_includes_to_sourcefile(self):
        self.__file.write(
            '#include "' + self.__file.create_mock_name('.h') + '"\n')
        self.__file.write(UNITY_INCLUDE + '\n')
        for custom_include in CUSTOM_INCLUDES:
            self.__file.write(custom_include + '\n')
        self.__file.write('#include <string.h>\n')
        self.__file.write('#include <stdlib.h>\n')
        self.__file.write('\n')

    def __write_defines_to_sourcefile(self):
        self.__file.write('#define MAX_LENGTH_ERROR_MESSAGE 100\n\n')

    def __write_global_vars_to_sourcefile(self, mockinfo):
        for mock in mockinfo:
            self.__file.write(
                'static ' + mock.function_name + 'MockData ' +
                mock.function_name + 'Data;\n')
        self.__file.write('\n')

    def __write_setup_and_teardown_to_sourcefile(self, mockinfo):
        function = self.__file.basename
        self.__file.write('void ' + function + '_MockSetup(void)\n')
        self.__file.write('{\n')
        for mock in mockinfo:
            initline = '    memset(&' + mock.function_name + \
                'Data, 0, sizeof(' + mock.function_name + 'Data));\n'
            self.__file.write(initline)
        self.__file.write('}\n\n')

        self.__file.write('void ' + function + '_MockTeardown(void)\n')
        self.__file.write('{\n')
        for mock in mockinfo:
            self.__file.write(
                '    TEST_ASSERT_EQUAL_MESSAGE(' + mock.function_name +
                'Data.ExpectedNrCalls,\n' + ' ' * 30 +
                mock.function_name + 'Data.CallCounter,\n' +
                ' ' * 30 + '"' + mock.function_name +
                ' was not called as often as specified!");\n')
        self.__file.write('}')

    def __write_expected_call_function(self, mock):
        nr_calls = mock.function_name + 'Data.ExpectedNrCalls'
        prototype = '\n\n\n' + \
            self.__proto.expected_call_prototype(mock, '') + '\n'
        self.__file.write(prototype)
        self.__file.write('{\n')
        if self.__is_string_parameter_in_function(mock):
            self.__file.write('    size_t length = 0;\n')
        self.__file.write('    char errormsg[MAX_LENGTH_ERROR_MESSAGE];\n')
        self.__file.write(
            '    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many ' +
            'calls to %s, max number is: %d", __FUNCTION__, ' +
            'MAX_NR_FUNCTION_CALLS);\n')
        self.__file.write('    TEST_ASSERT_TRUE_MESSAGE(' + nr_calls +
                          ' < MAX_NR_FUNCTION_CALLS, errormsg);\n')
        self.__write_null_tests_to_sourcefile(mock)
        self.__file.write('\n')
        self.__write_parameter_copy_lines_to_sourcefile(mock)
        self.__write_return_type_copy_lines_to_sourcefile(mock)
        self.__file.write('    ' + nr_calls + '++;\n')
        self.__file.write('}\n\n')

    def __is_string_parameter_in_function(self, mock):
        for parameter in mock.parameters:
            param_no_spaces = parameter.type.replace(' ', '')
            if param_no_spaces in ['constchar*', 'charconst*']:
                return True
        return False

    def __write_null_tests_to_sourcefile(self, mock):
        for parameter in mock.parameters:
            if parameter.type.find('*') >= 0:
                self.__file.write('    TEST_ASSERT_NOT_NULL_MESSAGE(' +
                                  parameter.name +
                                  ', "parameter should not be NULL");\n')
        if mock.return_type.find('*') >= 0:
            self.__file.write('    /* no TEST_ASSERT_NOT_NULL for ReturnValu' +
                              'e, you might want to return NULL! */\n')

    def __write_parameter_copy_lines_to_sourcefile(self, mock):
        for parameter in mock.parameters:
            nr_calls = mock.function_name + 'Data.' + parameter.name +\
                '[' + mock.function_name + 'Data.ExpectedNrCalls]'
            param_no_spaces = parameter.type.replace(' ', '')
            param_no_const = \
                self.__proto.remove_const_from_type(parameter.type)
            if param_no_spaces == 'constchar*' or \
                    param_no_spaces == 'charconst*':
                self.__file.write(
                    '    length = strlen(' + parameter.name + ');\n')
                self.__file.write(
                    '    ' + nr_calls + ' = malloc(length+1);\n')
                self.__file.write(
                    '    TEST_ASSERT_NOT_NULL_MESSAGE(' + nr_calls +
                    ', "could not allocate' + ' memory");\n')
                self.__file.write(
                    '    strcpy(' + nr_calls + ', ' + parameter.name + ');\n')
            elif param_no_const.find('*') >= 0:
                self.__file.write(
                    '    ' + nr_calls + ' = *' + parameter.name + ';\n')
            elif param_no_const.strip() != 'void':
                self.__file.write(
                    '    ' + nr_calls + ' = ' + parameter.name + ';\n')

    def __write_return_type_copy_lines_to_sourcefile(self, mock):
        if mock.return_type != 'void':
            self.__file.write('    ' + mock.function_name +
                              'Data.ReturnValue[' + mock.function_name +
                              'Data.ExpectedNrCalls] = ReturnValue;\n')

    def __write_mock_function(self, mock):
        nr_calls = mock.function_name + 'Data.ExpectedNrCalls'
        callCount = mock.function_name + 'Data.CallCounter'
        prototype = self.__make_mock_prototype(mock)
        self.__file.write(prototype)
        self.__file.write('{\n')
        self.__file.write('    char errormsg[MAX_LENGTH_ERROR_MESSAGE];\n\n')
        self.__file.write(
            '    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many ' +
            'calls to %s: expected %d calls, this is call nr %d", __FUNCTION' +
            '__, ' + nr_calls + ', ' + callCount + '+1);\n')
        self.__file.write('    TEST_ASSERT_TRUE_MESSAGE(' + callCount +
                          ' < ' + nr_calls + ', errormsg);\n')
        self.__file.write('\n')
        self.__write_parameter_lines_to_mock_function(mock)
        if mock.return_type == 'void':
            self.__file.write('    ' + callCount + '++;\n')
        else:
            self.__file.write('    return ' + mock.function_name +
                              'Data.ReturnValue[' + callCount + '++];\n')
        self.__file.write('}')

    def __write_parameter_lines_to_mock_function(self, mock):
        if not self.__proto.is_void_parameter(mock.parameters):
            self.__file.write(
                '    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE' +
                ', "Call to %s with unexpected parameter(s) in ' +
                'call nr %d", __FUNCTION__, ' + mock.function_name +
                'Data.CallCounter+1);\n')
            for param in mock.parameters:
                callCount = mock.function_name + 'Data.' + param.name +\
                    '[' + mock.function_name + 'Data.CallCounter]'
                if param.funcptr:
                    self.__file.write(
                        '    if (' + param.name + ' != NULL)' + ' TEST_' +
                        'ASSERT_EQUAL_PTR_MESSAGE(' + callCount + ', ' +
                        param.name + ', errormsg);\n')
                elif param.type.find('*') >= 0 and \
                        param.type.find('const') == -1:
                    # output parameter: copy expected data into param
                    self.__file.write(
                        '    *' + param.name + ' = ' + callCount + ';\n')
                else:
                    # input parameter: check if expected data is correct
                    param_no_spaces = param.type.replace(' ', '')
                    if param_no_spaces == 'constchar*' or \
                            param_no_spaces == 'charconst*':
                        self.__file.write(
                            '    TEST_ASSERT_EQUAL_STRING_MESSAGE(' +
                            callCount + ', ' + param.name + ', errormsg);\n')
                        self.__file.write('    free(' + callCount + ');\n')
                        self.__file.write('    ' + callCount + ' = NULL;\n')
                    elif param.type.find('*') >= 0:
                        type_without_const_or_ptr = param.type.replace(
                            'const', '').replace('*', '').strip()
                        unityTesttype = self.__find_unity_test_type(
                            type_without_const_or_ptr)
                        if unityTesttype is None:
                            self.__file.write(
                                '    TEST_ASSERT_EQUAL_MEMORY_MESSAGE(&(' +
                                callCount + '), ' + param.name + ', sizeof(*' +
                                param.name + '), errormsg);\n')
                        else:
                            self.__file.write(
                                '    ' + unityTesttype + '(' + callCount +
                                ', *' + param.name + ', errormsg);\n')
                    else:
                        unityTesttype = self.__find_unity_test_type(param.type)
                        if unityTesttype is None:
                            self.__file.write(
                                '    TEST_ASSERT_EQUAL_MEMORY_MESSAGE(&(' +
                                callCount + '), &' + param.name + ', sizeof(' +
                                param.name + '), errormsg);\n')
                        else:
                            self.__file.write(
                                '    ' + unityTesttype + '(' + callCount +
                                ', ' + param.name + ', errormsg);\n')

    def __make_mock_prototype(self, mock):
        prototype = mock.return_type + ' ' + mock.function_name + '('
        for parameter in mock.parameters:
            prototype += parameter.original + ', '
        # strip last ', '
        if prototype[-2:] == ', ':
            prototype = prototype[:-2]
        prototype += ')\n'
        return prototype

    def __find_unity_test_type(self, paramType):
        global CTYPE_TO_UNITY_ASSERT_MACRO
        for ctype in CTYPE_TO_UNITY_ASSERT_MACRO:
            if ctype[0] == paramType:
                return ctype[1]
        return None
