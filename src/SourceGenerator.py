from FileGenerator import *
from configuration import *


class SourceGenerator(FileGenerator):
    def __init__(self, headerfile, maxNrFunctionCalls, version):
        super(SourceGenerator, self).__init__(
            headerfile, '.c', maxNrFunctionCalls, version)

    def generate(self, mockinfo):
        self.writeIncludesToSourcefile()
        self.writeDefinesAndGlobalVarsToSourceFile(mockinfo)
        self.writeSetupAndTearDownToSourceFile(mockinfo)
        for mock in mockinfo:
            self.writeExpectedCallFunction(mock)
            self.writeMockFunction(mock)

    def writeIncludesToSourcefile(self):
        global UNITY_INCLUDE
        global CUSTOM_INCLUDES
        self.file.write('#include "' + self.file.createMockName('.h') + '"\n')
        self.file.write(UNITY_INCLUDE + '\n')
        for custom_include in CUSTOM_INCLUDES:
            self.file.write(custom_include + '\n')
        self.file.write('#include <string.h>\n')
        self.file.write('#include <stdlib.h>\n')
        self.file.write('\n')

    def writeDefinesAndGlobalVarsToSourceFile(self, mockinfo):
        self.file.write('#define MAX_LENGTH_ERROR_MESSAGE 100\n\n')
        for mock in mockinfo:
            self.file.write('static ' + mock.functionName +
                            'MockData ' + mock.functionName + 'Data;\n')
        self.file.write('\n')

    def writeSetupAndTearDownToSourceFile(self, mockinfo):
        function = self.headerfile[:self.headerfile.rfind('.')]
        self.file.write('void ' + function + '_MockSetup(void)\n')
        self.file.write('{\n')
        for mock in mockinfo:
            initline = '    memset(&' + mock.functionName + \
                'Data, 0, sizeof(' + mock.functionName + 'Data));\n'
            self.file.write(initline)
        self.file.write('}\n\n')

        self.file.write('void ' + function + '_MockTeardown(void)\n')
        self.file.write('{\n')
        for mock in mockinfo:
            assertline = '    TEST_ASSERT_EQUAL_MESSAGE(' + \
                mock.functionName + 'Data.ExpectedNrCalls,\n'
            assertline += '                              ' + \
                mock.functionName + 'Data.CallCounter,\n'
            assertline += '                              "' + \
                mock.functionName + \
                ' was not called as often as specified!");\n'
            self.file.write(assertline)
        self.file.write('}')

    def writeExpectedCallFunction(self, mock):
        nrCalls = mock.functionName + 'Data.ExpectedNrCalls'
        prototype = '\n\n\n' + self.makeExpectedCallPrototype(mock, '') + '\n'
        self.file.write(prototype)
        self.file.write('{\n')
        if self.stringParameterInFunction(mock):
            self.file.write('    size_t length = 0;\n')
        self.file.write('    char errormsg[MAX_LENGTH_ERROR_MESSAGE];\n')
        self.file.write(
            '    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many ' +
            'calls to %s, max number is: %d", __FUNCTION__, ' +
            'MAX_NR_FUNCTION_CALLS);\n')
        self.file.write('    TEST_ASSERT_TRUE_MESSAGE(' + nrCalls +
                        ' < MAX_NR_FUNCTION_CALLS, errormsg);\n')
        self.writeNullTestsToSourceFile(mock)
        self.file.write('\n')
        self.writeParameterCopyLinesToSourceFile(mock)
        self.writeReturnTypeCopyLinesToSourceFile(mock)
        self.file.write('    ' + nrCalls + '++;\n')
        self.file.write('}\n\n')

    def stringParameterInFunction(self, mock):
        for parameter in mock.parameters:
            paramNoSpaces = parameter.type.replace(' ', '')
            if paramNoSpaces == 'constchar*' or paramNoSpaces == 'charconst*':
                return True
        return False

    def writeNullTestsToSourceFile(self, mock):
        for parameter in mock.parameters:
            if parameter.type.find('*') >= 0:
                self.file.write('    TEST_ASSERT_NOT_NULL_MESSAGE(' +
                                parameter.name +
                                ', "parameter should not be NULL");\n')
        if mock.returnType.find('*') >= 0:
            self.file.write('    /* no TEST_ASSERT_NOT_NULL for ReturnValue,' +
                            ' you might want to return NULL! */\n')

    def writeParameterCopyLinesToSourceFile(self, mock):
        for parameter in mock.parameters:
            nrCalls = mock.functionName + 'Data.' + parameter.name +\
                '[' + mock.functionName + 'Data.ExpectedNrCalls]'
            paramNoSpaces = parameter.type.replace(' ', '')
            paramNoConst = self.removeConstFromType(parameter.type)
            if paramNoSpaces == 'constchar*' or paramNoSpaces == 'charconst*':
                self.file.write(
                    '    length = strlen(' + parameter.name + ');\n')
                self.file.write('    ' + nrCalls +
                                ' = malloc(length+1);\n')
                self.file.write('    TEST_ASSERT_NOT_NULL_MESSAGE(' +
                                nrCalls + ', "could not allocate' +
                                ' memory");\n')
                self.file.write('    strcpy(' + nrCalls + ', ' +
                                parameter.name + ');\n')
            elif paramNoConst.find('*') >= 0:
                self.file.write('    ' + nrCalls + ' = *' +
                                parameter.name + ';\n')
            elif paramNoConst.strip() != 'void':
                self.file.write('    ' + nrCalls + ' = ' +
                                parameter.name + ';\n')

    def writeReturnTypeCopyLinesToSourceFile(self, mock):
        if mock.returnType != 'void':
            self.file.write('    ' + mock.functionName +
                            'Data.ReturnValue[' + mock.functionName +
                            'Data.ExpectedNrCalls] = ReturnValue;\n')

    def writeMockFunction(self, mock):
        nrCalls = mock.functionName + 'Data.ExpectedNrCalls'
        callCount = mock.functionName + 'Data.CallCounter'
        prototype = self.makeMockPrototype(mock)
        self.file.write(prototype)
        self.file.write('{\n')
        self.file.write('    char errormsg[MAX_LENGTH_ERROR_MESSAGE];\n\n')
        self.file.write('    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, ' +
                        '"Too many calls to %s: expected %d calls, this is' +
                        ' call nr %d", __FUNCTION__, ' + nrCalls +
                        ', ' + callCount + '+1);\n')
        self.file.write('    TEST_ASSERT_TRUE_MESSAGE(' + callCount +
                        ' < ' + nrCalls + ', errormsg);\n')
        self.file.write('\n')
        self.writeParameterLinesToMockFunction(mock)
        if mock.returnType == 'void':
            self.file.write('    ' + callCount + '++;\n')
        else:
            self.file.write('    return ' + mock.functionName +
                            'Data.ReturnValue[' + callCount + '++];\n')
        self.file.write('}')

    def writeParameterLinesToMockFunction(self, mock):
        if not self.isVoidParameter(mock.parameters):
            self.file.write('    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE' +
                            ', "Call to %s with unexpected parameter(s) in ' +
                            'call nr %d", __FUNCTION__, ' + mock.functionName +
                            'Data.CallCounter+1);\n')
            for param in mock.parameters:
                callCount = mock.functionName + 'Data.' + param.name +\
                    '[' + mock.functionName + 'Data.CallCounter]'
                if param.funcptr:
                    self.file.write('    if (' + param.name + ' != NULL)' +
                                    ' TEST_ASSERT_EQUAL_PTR_MESSAGE(' +
                                    callCount + ', ' + param.name +
                                    ', errormsg);\n')
                elif param.type.find('*') >= 0 and \
                        param.type.find('const') == -1:
                    # output parameter: copy expected data into param
                    self.file.write('    *' + param.name + ' = ' +
                                    callCount + ';\n')
                else:
                    # input parameter: check if expected data is correct
                    paramNoSpaces = param.type.replace(' ', '')
                    if paramNoSpaces == 'constchar*' or \
                            paramNoSpaces == 'charconst*':
                        self.file.write('    TEST_ASSERT_EQUAL_STRING_MESSAG' +
                                        'E(' + callCount + ', ' +
                                        param.name + ', errormsg);\n')
                        self.file.write('    free(' + callCount + ');\n')
                        self.file.write('    ' + callCount + ' = NULL;\n')
                    elif param.type.find('*') >= 0:
                        typeWithoutConstOrPtr = param.type.replace(
                            'const', '').replace('*', '').strip()
                        unityTesttype = self.findUnityTestType(
                            typeWithoutConstOrPtr)
                        if unityTesttype is None:
                            self.file.write('    TEST_ASSERT_EQUAL_MEMORY_ME' +
                                            'SSAGE(&(' + callCount + '), ' +
                                            param.name + ', sizeof(*' +
                                            param.name + '), errormsg);\n')
                        else:
                            self.file.write('    ' + unityTesttype + '(' +
                                            callCount + ', *' + param.name +
                                            ', errormsg);\n')
                    else:
                        unityTesttype = self.findUnityTestType(param.type)
                        if unityTesttype is None:
                            self.file.write('    TEST_ASSERT_EQUAL_MEMORY_ME' +
                                            'SSAGE(&(' + callCount + '), &' +
                                            param.name + ', sizeof(' +
                                            param.name + '), errormsg);\n')
                        else:
                            self.file.write('    ' + unityTesttype + '(' +
                                            callCount + ', ' + param.name +
                                            ', errormsg);\n')

    def makeMockPrototype(self, mock):
        prototype = mock.returnType + ' ' + mock.functionName + '('
        for parameter in mock.parameters:
            prototype += parameter.original + ', '
        # strip last ', '
        if prototype[-2:] == ', ':
            prototype = prototype[:-2]
        prototype += ')\n'
        return prototype

    def findUnityTestType(self, paramType):
        global CTYPE_TO_UNITY_ASSERT_MACRO
        for ctype in CTYPE_TO_UNITY_ASSERT_MACRO:
            if ctype[0] == paramType:
                return ctype[1]
        return None
