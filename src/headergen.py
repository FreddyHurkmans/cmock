from cfile_writer import CFileWriter
from protogen import PrototypeGenerator


class HeaderGenerator(object):
    def __init__(self, input_header, max_nr_function_calls, version):
        self.__max_nr_function_calls = max_nr_function_calls
        self.__proto = PrototypeGenerator()
        self.__file = CFileWriter(input_header, '.h', version)

    def __del__(self):
        self.__write_footer()

    def generate(self, mockinfo):
        self.__write_multiple_include_protection()
        self.__write_includes()
        self.__write_defines()
        self.__write_structs_to_headerfile(mockinfo)
        self.__write_prototypes_to_headerfile(mockinfo)

    def __write_structs_to_headerfile(self, mockinfo):
        for mock in mockinfo:
            self.__file.write('typedef struct\n')
            self.__file.write('{\n')
            if not (len(mock.parameters) == 1 and
                    mock.parameters[0].type.strip() == 'void'):
                self.__file.write('    /* parameters */\n')
            for parameter in mock.parameters:
                self.__write_parameter_info_to_struct(parameter)
            if mock.return_type != 'void':
                self.__file.write('    /* return value */\n')
                self.__file.write('    ' + self.__proto.remove_const_from_type(
                    mock.return_type) +
                    ' ReturnValue[MAX_NR_FUNCTION_CALLS];\n')
            self.__file.write('    /* administration */\n')
            self.__file.write('    int CallCounter;\n')
            self.__file.write('    int ExpectedNrCalls;\n')
            self.__file.write('} ' + mock.function_name + 'MockData;\n\n')

    def __write_parameter_info_to_struct(self, param):
        if param.type.strip() != 'void':
            param_no_spaces = param.type.replace(' ', '')
            if param.funcptr:
                temp = param.original.replace(
                    param.name, param.name + '[MAX_NR_FUNCTION_CALLS]')
                self.__file.write('    ' + temp + ';\n')
            elif param_no_spaces == 'constchar*' or \
                    param_no_spaces == 'charconst*':
                self.__file.write('    char* ' + param.name +
                                  '[MAX_NR_FUNCTION_CALLS];\n')
            else:
                param_type = param.type.replace('const', '')
                while param_type.find('  ') >= 0:
                    param_type = param_type.replace('  ', ' ')
                param_type = param_type.replace('*', '').strip()
                self.__file.write('    ' + param_type + ' ' +
                                  param.name + '[MAX_NR_FUNCTION_CALLS];\n')

    def __write_prototypes_to_headerfile(self, mockinfo):
        first_part = 'void ' + self.__file.basename + '_Mock'
        self.__file.write(first_part + 'Setup(void);' +
                          '    /* call this from the Setup of your test! */\n')
        self.__file.write(first_part + 'Teardown(void);' +
                          ' /* call this from the Teardown of your test! */\n')
        self.__file.write('\n')
        self.__file.write(
            '/* call these for each call you expect for a given function */')
        for mock in mockinfo:
            prototype = '\n' + self.__proto.expected_call_prototype(mock, ';')
            self.__file.write(prototype)

    def __multiple_include_name(self):
        return self.__file.filename.upper().replace('.', '_')

    def __write_multiple_include_protection(self):
        defineName = self.__multiple_include_name()
        self.__file.write('#ifndef ' + defineName + '\n')
        self.__file.write('#define ' + defineName + '\n')
        self.__file.write('\n')

    def __write_includes(self):
        self.__file.write('#include "' + self.__file.input_header + '"\n\n')
        self.__write_system_includes()
        self.__file.write('\n')

    def __write_system_includes(self):
        # todo: move to configuration
        self.__file.write('#include <stdbool.h>\n')
        self.__file.write('#include <stdint.h>\n')

    def __write_defines(self):
        self.__file.write('#define MAX_NR_FUNCTION_CALLS ' +
                          self.__max_nr_function_calls + '\n')
        self.__file.write('\n')

    def __write_footer(self):
        self.__file.write('\n\n#endif  /* ' +
                          self.__multiple_include_name() + ' */')
