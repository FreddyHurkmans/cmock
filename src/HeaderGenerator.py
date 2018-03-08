from FileGenerator import *


class HeaderGenerator(FileGenerator):
    def __init__(self, headerfile, maxNrFunctionCalls, version):
        super(HeaderGenerator, self).__init__(
            headerfile, '.h', maxNrFunctionCalls, version)

    def generate(self, mockinfo):
        self.writeStructsToHeaderfile(mockinfo)
        self.writePrototypesToHeaderfile(mockinfo)

    def writeStructsToHeaderfile(self, mockinfo):
        for mock in mockinfo:
            self.file.write('typedef struct\n')
            self.file.write('{\n')
            if not (len(mock.parameters) == 1 and
                    mock.parameters[0].type.strip() == 'void'):
                self.file.write('    /* parameters */\n')
            for parameter in mock.parameters:
                self.writeParameterInfoToStruct(parameter)
            if mock.returnType != 'void':
                self.file.write('    /* return value */\n')
                self.file.write('    ' + self.removeConstFromType(
                    mock.returnType) +
                    ' ReturnValue[MAX_NR_FUNCTION_CALLS];\n')
            self.file.write('    /* administration */\n')
            self.file.write('    int CallCounter;\n')
            self.file.write('    int ExpectedNrCalls;\n')
            self.file.write('} ' + mock.functionName + 'MockData;\n\n')

    def writeParameterInfoToStruct(self, parameter):
        if parameter.type.strip() != 'void':
            paramNoSpaces = parameter.type.replace(' ', '')
            if parameter.funcptr:
                temp = parameter.original.replace(
                    parameter.name, parameter.name + '[MAX_NR_FUNCTION_CALLS]')
                self.file.write('    ' + temp + ';\n')
            elif paramNoSpaces == 'constchar*' or \
                    paramNoSpaces == 'charconst*':
                self.file.write('    char* ' + parameter.name +
                                '[MAX_NR_FUNCTION_CALLS];\n')
            else:
                paramType = parameter.type.replace('const', '')
                while paramType.find('  ') >= 0:
                    paramType = paramType.replace('  ', ' ')
                paramType = paramType.replace('*', '').strip()
                self.file.write('    ' + paramType + ' ' +
                                parameter.name + '[MAX_NR_FUNCTION_CALLS];\n')

    def writePrototypesToHeaderfile(self, mockinfo):
        self.headerfile = self.headerfile[:self.headerfile.rfind('.')]
        self.file.write('void ' + self.headerfile +
                        '_MockSetup(void);' +
                        '    /* call this from the Setup of your test! */\n')
        self.file.write('void ' + self.headerfile +
                        '_MockTeardown(void);' +
                        ' /* call this from the Teardown of your test! */\n\n')
        self.file.write(
            '/* call these for each call you expect for a given function */')
        for mock in mockinfo:
            prototype = '\n' + self.makeExpectedCallPrototype(mock, ';')
            self.file.write(prototype)
