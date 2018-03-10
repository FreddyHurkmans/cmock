from configuration import Config
from type_determination import Type


class MockCodeGenerator(object):
    def __init__(self, file, proto, mock):
        self.__file = file
        self.__proto = proto
        self.__mock = mock

    def generate(self):
        nr_calls = self.__mock.function_name + 'Data.ExpectedNrCalls'
        callCount = self.__mock.function_name + 'Data.CallCounter'
        prototype = self.__make_mock_prototype()
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
        self.__write_parameter_lines_to_mock_function()
        if self.__mock.return_type == 'void':
            self.__file.write('    ' + callCount + '++;\n')
        else:
            self.__file.write('    return ' + self.__mock.function_name +
                              'Data.ReturnValue[' + callCount + '++];\n')
        self.__file.write('}')

    def __write_parameter_lines_to_mock_function(self):
        if not self.__proto.is_void_parameter(self.__mock.parameters):
            self.__file.write(
                '    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE' +
                ', "Call to %s with unexpected parameter(s) in ' +
                'call nr %d", __FUNCTION__, ' + self.__mock.function_name +
                'Data.CallCounter+1);\n')
            for param in self.__mock.parameters:
                callCount = self.__mock.function_name + 'Data.' + param.name +\
                    '[' + self.__mock.function_name + 'Data.CallCounter]'
                param_no_spaces = param.type.replace(' ', '')
                if param.funcptr:
                    self.__file.write(
                        '    if (' + param.name + ' != NULL)' + ' TEST_' +
                        'ASSERT_EQUAL_PTR_MESSAGE(' + callCount + ', ' +
                        param.name + ', errormsg);\n')
                elif Type.is_string(param_no_spaces):
                    self.__file.write(
                        '    TEST_ASSERT_EQUAL_STRING_MESSAGE(' +
                        callCount + ', ' + param.name + ', errormsg);\n')
                    self.__file.write('    free(' + callCount + ');\n')
                    self.__file.write('    ' + callCount + ' = NULL;\n')
                elif Type.is_output_pointer(param.type):
                    # output parameter: copy expected data into param
                    self.__file.write(
                        '    *' + param.name + ' = ' + callCount + ';\n')
                elif Type.is_pointer(param.type):
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

    def __make_mock_prototype(self):
        prototype = self.__mock.return_type + ' ' + \
            self.__mock.function_name + '('
        for parameter in self.__mock.parameters:
            prototype += parameter.original + ', '
        # strip last ', '
        if prototype[-2:] == ', ':
            prototype = prototype[:-2]
        prototype += ')\n'
        return prototype

    def __find_unity_test_type(self, paramType):
        for ctype in Config.CTYPE_TO_UNITY_ASSERT_MACRO:
            if ctype[0] == paramType:
                return ctype[1]
        return None
