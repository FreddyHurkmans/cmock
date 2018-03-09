class PrototypeGenerator(object):
    def expected_call_prototype(self, mock, line_ending):
        prototype = 'void ' + mock.function_name + '_ExpectedCall('
        # parameters
        funcptr_parameter_found = False
        if (self.is_void_parameter(mock.parameters)) and \
                (mock.return_type == 'void'):
            prototype += 'void'
        elif (not self.is_void_parameter(mock.parameters)):
            for parameter in mock.parameters:
                if parameter.funcptr:
                    funcptr_parameter_found = True
                param = parameter.original
                if (not parameter.funcptr) and (param.find('*') >= 0) and \
                        (param.find('const') < 0):
                    param = 'const ' + param
                prototype += param + ', '
        # return value
        if mock.return_type != 'void':
            prototype += self.remove_const_from_type(
                mock.return_type) + ' ReturnValue'
        # strip last ', '
        if prototype[-2:] == ', ':
            prototype = prototype[:-2]

        prototype += ')' + line_ending
        if funcptr_parameter_found:
            prototype += ' /* if you don\'t want to check function ' \
                'pointer(s), make it NULL */'
        return prototype

    def remove_const_from_type(self, ctype):
        ctype = ctype.replace('const', '').strip()
        while ctype.find('  ') >= 0:
            ctype = ctype.replace('  ', ' ')
        return ctype

    def is_void_parameter(self, parameterlist):
        return (len(parameterlist) == 1) and (parameterlist[0].type == 'void')
