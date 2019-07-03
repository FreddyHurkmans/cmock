from cfile_writer import CFileWriter
from expected_call import ExpectedCallGenerator
from mock_code import MockCodeGenerator
from protogen import PrototypeGenerator
from configuration import Config


class SourceGenerator(object):
    def __init__(self, input_header):
        self.__proto = PrototypeGenerator()
        self.__file = CFileWriter(input_header, '.c')

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
        self.__file.write(Config.UNITY_INCLUDE + '\n')
        for custom_include in Config.CUSTOM_INCLUDES:
            self.__file.write(custom_include + '\n')
        self.__file.write('#include <string.h>\n')
        self.__file.write('#include <stdlib.h>\n')
        self.__file.write('\n')

    def __write_defines_to_sourcefile(self):
        self.__file.write('#define MAX_LENGTH_ERROR_MESSAGE 100\n\n')

    def __write_global_vars_to_sourcefile(self, mockinfo):
        for mock in mockinfo:
            self.__file.write(
                'static ' + mock.function_name + '_MockData ' +
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
        function = ExpectedCallGenerator(self.__file, self.__proto, mock)
        function.generate()

    def __write_mock_function(self, mock):
        function = MockCodeGenerator(self.__file, self.__proto, mock)
        function.generate()
