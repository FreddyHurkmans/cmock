class ExpectedCallGenerator(object):
    def __init__(self, file, proto, mock):
        self.__file = file
        self.__proto = proto
        self.__mock = mock

    def generate(self):
        nr_calls = self.__mock.function_name + 'Data.ExpectedNrCalls'
        prototype = '\n\n\n' + \
            self.__proto.expected_call_prototype(self.__mock, '') + '\n'
        self.__file.write(prototype)
        self.__file.write('{\n')
        if self.__is_string_parameter_in_function():
            self.__file.write('    size_t length = 0;\n')
        self.__file.write('    char errormsg[MAX_LENGTH_ERROR_MESSAGE];\n')
        self.__file.write(
            '    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many ' +
            'calls to %s, max number is: %d", __FUNCTION__, ' +
            'MAX_NR_FUNCTION_CALLS);\n')
        self.__file.write('    TEST_ASSERT_TRUE_MESSAGE(' + nr_calls +
                          ' < MAX_NR_FUNCTION_CALLS, errormsg);\n')
        self.__write_null_tests_to_sourcefile()
        self.__file.write('\n')
        self.__write_parameter_copy_lines_to_sourcefile()
        self.__write_return_type_copy_lines_to_sourcefile()
        self.__file.write('    ' + nr_calls + '++;\n')
        self.__file.write('}\n\n')

    def __is_string_parameter_in_function(self):
        for parameter in self.__mock.parameters:
            param_no_spaces = parameter.type.replace(' ', '')
            if param_no_spaces in ['constchar*', 'charconst*']:
                return True
        return False

    def __write_null_tests_to_sourcefile(self):
        for parameter in self.__mock.parameters:
            if parameter.type.find('*') >= 0:
                self.__file.write('    TEST_ASSERT_NOT_NULL_MESSAGE(' +
                                  parameter.name +
                                  ', "parameter should not be NULL");\n')
        if self.__mock.return_type.find('*') >= 0:
            self.__file.write('    /* no TEST_ASSERT_NOT_NULL for ReturnValu' +
                              'e, you might want to return NULL! */\n')

    def __write_parameter_copy_lines_to_sourcefile(self):
        for parameter in self.__mock.parameters:
            nr_calls = self.__mock.function_name + 'Data.' + parameter.name +\
                '[' + self.__mock.function_name + 'Data.ExpectedNrCalls]'
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

    def __write_return_type_copy_lines_to_sourcefile(self):
        if self.__mock.return_type != 'void':
            self.__file.write('    ' + self.__mock.function_name +
                              'Data.ReturnValue[' + self.__mock.function_name +
                              'Data.ExpectedNrCalls] = ReturnValue;\n')
