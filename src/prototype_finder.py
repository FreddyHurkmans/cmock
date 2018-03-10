import subprocess
from configuration import Config


class MockInfoStruct:
    # MockInfo is used as a struct, it will contain:
    # field          type
    # ------------------------
    # .function_name string
    # .return_type   string
    # .funcptr       bool (returntype is funcptr)
    # .parameters    list of ParamInfo
    pass


class ParamInfoStruct:
    # ParamInfo is used as a struct, it will contain:
    # field          type
    # ------------------------
    # .original      string
    # .type          string
    # .name          string
    # .funcptr       bool
    pass


class PrototypeFinder(object):
    def __init__(self, headerfile):
        self.__headerfile = headerfile
        self.__find_prototypes()

    def any_prototypes_found(self):
        return len(self.__ctags_output) > 0

    def get_mock_info(self):
        mockinfo = []
        for prototype in self.__ctags_output:
            prototype = prototype[prototype.find(self.__headerfile) +
                                  len(self.__headerfile) + 1:].strip()
            prototype = self.__remove_extern_keyword(prototype)
            left_part = prototype[:prototype.find('(')]

            # todo: move this to MockInfo class
            mock = MockInfoStruct()
            (mock.function_name, mock.return_type, mock.funcptr) = \
                self.__split_parameter_type_and_name(left_part)
            parameter_list = self.__split_parameter_list(prototype)
            mock.parameters = []
            for parameter in parameter_list:
                paraminfo = ParamInfoStruct()
                paraminfo.original = parameter.strip()
                (paraminfo.name, paraminfo.type, paraminfo.funcptr) = \
                    self.__split_parameter_type_and_name(paraminfo.original)
                mock.parameters.append(paraminfo)
            mockinfo.append(mock)
        return mockinfo

    def __find_prototypes(self):
        self.__ctags_output = str(subprocess.check_output(
            [Config.CTAGS_EXECUTABLE, '-x', '-u', '--c-kinds=fp',
                self.__headerfile]))
        self.__ctags_output = self.__ctags_output.split('\\n')
        self.__ctags_output = self.__ctags_output[:-1]

    def __remove_extern_keyword(self, prototype):
        if prototype.find('extern') == 0:
            prototype = prototype[6:].strip()
        return prototype

    def __split_parameter_type_and_name(self, parameter):
        funcptr = False
        if parameter.strip() == 'void':
            param_name = ''
            param_type = 'void'
        elif parameter.find('(') >= 0:
            # function pointer
            funcptr = True
            # int **(*callback)(int** p)
            param_name = parameter[parameter.find('(') + 1:
                                   parameter.find(')')].strip('*')
            param_type = ''
        else:
            lastSpace = parameter.rfind(' ')
            lastStar = parameter.rfind('*')
            param_name = parameter[max(lastSpace, lastStar) + 1:].strip()
            param_type = parameter[:parameter.rfind(param_name)].strip()
        return [param_name, param_type, funcptr]

    def __split_parameter_list(self, prototype):
        prototype = prototype[prototype.find('(') + 1:
                              prototype.rfind(')')].strip()
        parameter_list = []
        # function_pointer builds function_pointer parameter, can be split over
        # multiple parameters due to split on comma!
        function_pointer = ''
        # function_pointer_bracket_count remembers the number of brackets in
        # functionptr that are still open (should become 0 at end of
        # functionptr)
        function_pointer_bracket_count = 0
        for parameter in prototype.split(','):
            if function_pointer_bracket_count == 0 and \
                    parameter.count('(') == 0:
                # no function pointer
                parameter_list.append(parameter)
            else:
                # part of function pointer
                function_pointer_bracket_count += parameter.count(
                    '(') - parameter.count(')')
                function_pointer += parameter + ','
                if function_pointer_bracket_count == 0:
                    parameter_list.append(function_pointer[:-1])
                    function_pointer = ''
        return parameter_list
