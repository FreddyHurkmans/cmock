#!/usr/bin/python

DESCRIPTION = 'Mock generator for c code'
VERSION     = '0.2'
AUTHOR      = 'Freddy Hurkmans'
LICENSE     = 'BSD 3-Clause'

# NOTES:
# This is a rather straight forward mock generator with the following limitations:
# - it depends on ctags to read function prototypes from the given headerfile
# - array parameters are NOT SUPPORTED
# - pointers to pointers are NOT SUPPORTED
# - const pointer parameters (e.g. const MYTYPE*) are considered to be input parameters, const char* types are
#   considered to be input strings
# - pointer parameters (e.g. MYTYPE*) are considered to be output parameters, char* types are considered to be
#   output chars, thus no string (remember: arrays are not supported!)
# - strings currently have a maximum string length (hardcoded in MaxStringLength: 200), this will
#   change to dynamically allocated memory in the next version
#
# for mock generation, this means that:
# int foo(const MYTYPE* bar);
# will generate a mock foo function and a function to indicate expected calls:
# void foo_ExpectedCall(const MYTYPE* bar, int ReturnValue)
# In this case: bar is a const pointer type. Thus it is considered to be an input parameter. In the ExpectedCall
# function bar is copied into local memory of type MYTYPE and in the mock foo function, bar is checked against the
# expected value.
#
# THE OTHER CASE:
# int foo(MYTYPE* bar);
# will also generate a mock foo function and a function to indicate expected calls:
# void foo_ExpectedCall(const MYTYPE* bar, int ReturnValue)
# In this case: bar is a non-const pointer type. Thus it is considered to be an output parameter. In the ExpectedCall
# function bar is copied into local memory of type MYTYPE and in the mock foo function, the copied bar data is copied
# into the dereferenced bar parameter.

import sys
import subprocess
from time import strftime

# List of all supported c types and the matching unity ASSERT macro's
# If these types have different sizes on your system, you can simply correct
# the macros. If you have missing types, you can simply add your type/macro pairs
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


# set defaults for parameters
Verbose = False
MaxNrFunctionCalls = '25'
MaxStringLength = '200'

CTAGS_EXECUTABLE = 'ctags'
UNITY_INCLUDE = '#include "unity.h"'
#CUSTOM_INCLUDES = ['#include "resource_detector.h"']
CUSTOM_INCLUDES = []


################### PRINT METHODS ##############################################
def printf(line):
    # prints to stdout if Verbose is set
    global Verbose
    if Verbose:
        print line

def printMockInfo(mockinfo):
    printf('FUNCTION\t\tRETURN TYPE\t\tPARAMETER LIST')
    for mock in mockinfo:
        line = mock.functionName + '\t\t' + mock.returnType + '\t\t'
        for parameter in mock.parameters:
            line += parameter.type + ' ' + parameter.name + ', '
        printf(line[:-2])

def printerror(lineparts):
    # prints to stderr and exits
    sys.stderr.write('\n')
    for part in lineparts:
        sys.stderr.write(str(part))
    sys.stderr.write('\n\n')
    sys.exit()


################################################################################
################### CLASSES ####################################################
################################################################################

class FileWriter(object):
    def __init__(self, sourcefilename, extension, maxNrFunctionCalls):
        self.sourcefilename = self.getBasename(sourcefilename)
        self.filename = self.createMockName(extension)
        self.maxNrFunctionCalls = maxNrFunctionCalls
        self.fd = open(self.filename, 'w')
        self.writeHeader()

    def __del__(self):
        self.writeFooter()
        self.fd.close()

    def getBasename(self, path):
        path = path.replace('\\', '/').rstrip('/')
        return path[path.rfind('/')+1:]

    def createMockName(self, extension):
        return self.sourcefilename[:self.sourcefilename.rfind('.')] + '_mock' + extension

    def writeHeader(self):
        self.writeGenericHeader()
        if self.filename[-2:] == '.h':
            self.writeHeaderfileExtras()

    def writeGenericHeader(self):
        global VERSION
        self.fd.write('/' + '*' * 79 + '\n')
        self.fd.write(' * generated code, please do not edit directly\n')
        self.fd.write(' * cMock version ' + VERSION + ' written by Freddy Hurkmans\n')
        self.fd.write(' *\n')
        self.fd.write(' * source file    : ' + self.sourcefilename + '\n')
        self.fd.write(' * filename       : ' + self.filename + '\n')
        self.fd.write(' * generation date: ' + strftime('%d %b %Y - %H:%M:%S') + '\n')
        self.fd.write(' *\n')
        self.fd.write(' ' + '*' * 78 + '/\n\n')

    def writeHeaderfileExtras(self):
        defineName = self.headerProtectionDefine()
        self.fd.write('#ifndef ' + defineName + '\n')
        self.fd.write('#define ' + defineName + '\n\n')
        self.writeSystemIncludes()
        self.fd.write('\n#include "' + self.sourcefilename + '"\n\n')
        self.fd.write('#define MAX_NR_FUNCTION_CALLS ' + self.maxNrFunctionCalls + '\n')
        self.fd.write('#define MAX_STRING_LENGTH ' + MaxStringLength + '\n\n')

    def headerProtectionDefine(self):
        return '__' + self.filename.upper().replace('.', '_')

    def writeSystemIncludes(self):
        self.fd.write('#include <stdbool.h>\n')
        self.fd.write('#include <stdint.h>\n')

    def writeFooter(self):
        if self.filename[-2:] == '.h':
            self.fd.write('\n\n#endif  /* ' + self.headerProtectionDefine() + ' */')
        self.fd.write('\n')  

    def write(self, line):
        self.fd.write(line)      

################################################################################

class MockInfo:
    # MockInfo is used as a struct, it will contain:
    # field          type
    # ------------------------
    # .functionName  string
    # .returnType    string
    # .parameters    list of ParamInfo
    pass

class ParamInfo:
    # ParamInfo is used as a struct, it will contain:
    # field          type
    # ------------------------
    # .original      string
    # .type          string
    # .name          string
    pass


################################################################################

class Prototypes(object):
    def __init__(self, headerfile):
        self.headerfile = headerfile
        self.getPrototypesUsingCtags()
   
    def getPrototypesUsingCtags(self):
        global CTAGS_EXECUTABLE
        self.ctagsOutput = subprocess.check_output([CTAGS_EXECUTABLE, '-x', '-u', '--c-kinds=fp', self.headerfile])
        self.ctagsOutput = self.ctagsOutput.split('\n')
        self.ctagsOutput = self.ctagsOutput[:-1]

    def anyPrototypesFound(self):
        return len(self.ctagsOutput) > 0

    def getMockInfo(self):
        mockinfo = []
        for prototype in self.ctagsOutput:
            prototype = prototype[prototype.find(self.headerfile) + len(self.headerfile) + 1:].strip()
            prototype = self.removeExternKeyword(prototype)
            leftPart = prototype[:prototype.find('(')]

            mock = MockInfo()
            (mock.functionName, mock.returnType) = self.splitParameterTypeAndName(leftPart)
            mock.parameters = []
            for parameter in prototype[prototype.find('(')+1:prototype.find(')')].strip().split(','):
                paraminfo = ParamInfo()
                paraminfo.original = parameter.strip()
                (paraminfo.name, paraminfo.type) = self.splitParameterTypeAndName(paraminfo.original)
                mock.parameters.append(paraminfo)
            mockinfo.append(mock)
        return mockinfo

    def removeExternKeyword(self, prototype):
        if prototype.find('extern') == 0:
            prototype = prototype[6:].strip()
        return prototype

    def splitParameterTypeAndName(self, parameter):
        if parameter.strip() == 'void':
            paramName = ''
            paramType = 'void'
        else:
            lastSpace = parameter.rfind(' ')
            lastStar = parameter.rfind('*')
            paramName = parameter[max(lastSpace, lastStar)+1:].strip()
            paramType = parameter[:parameter.rfind(paramName)].strip()
        return [paramName, paramType]


################################################################################

class FileGenerator(object):
    def __init__(self, headerfile, kind, maxNrFunctionCalls):
        self.headerfile = headerfile
        self.file = FileWriter(headerfile, kind, maxNrFunctionCalls)

    def removeConstFromType(self, ctype):
        ctype = ctype.replace('const', '').strip()
        while ctype.find('  ') >= 0:
            ctype = ctype.replace('  ', ' ')
        return ctype

    def makePrototype(self, mock):
        prototype = 'void ' + mock.functionName + '_ExpectedCall('
        # parameters
        if (self.isVoidParameter(mock.parameters)) and (mock.returnType == 'void'):
            prototype += 'void'
        elif (not self.isVoidParameter(mock.parameters)):
            for parameter in mock.parameters:
                param = parameter.original
                if (param.find('*') >= 0) and (param.find('const') < 0):
                    param = 'const ' + param
                prototype += param + ', '
        # return value
        if mock.returnType != 'void':
            prototype += self.removeConstFromType(mock.returnType) + ' ReturnValue'
        # strip last ', '
        if prototype[-2:] == ', ':
            prototype = prototype[:-2]
        return prototype + ')'

    def isVoidParameter(self, parameterlist):
        return (len(parameterlist) == 1) and (parameterlist[0].type == 'void')


################################################################################

class HeaderGenerator(FileGenerator):
    def __init__(self, headerfile, maxNrFunctionCalls):
        super(HeaderGenerator, self).__init__(headerfile, '.h', maxNrFunctionCalls)

    def generate(self, mockinfo):
        self.writeStructsToHeaderfile(mockinfo)
        self.writePrototypesToHeaderfile(mockinfo)

    def writeStructsToHeaderfile(self, mockinfo):
        for mock in mockinfo:
            self.file.write('typedef struct\n')
            self.file.write('{\n')
            if not (len(mock.parameters) == 1 and mock.parameters[0].type.strip() == 'void'):
                self.file.write('    /* parameters */\n')
            for parameter in mock.parameters:
                self.writeParameterInfoToStruct(parameter)
            if mock.returnType != 'void':
                self.file.write('    /* return value */\n')
                self.file.write('    ' + self.removeConstFromType(mock.returnType) + ' ReturnValue[MAX_NR_FUNCTION_CALLS];\n')
            self.file.write('    /* administration */\n')
            self.file.write('    int CallCounter;\n')
            self.file.write('    int ExpectedNrCalls;\n')
            self.file.write('} ' + mock.functionName + 'Struct;\n\n')

    def writeParameterInfoToStruct(self, parameter):
        if parameter.type.strip() != 'void':
            paramNoSpaces = parameter.type.replace(' ', '')
            if paramNoSpaces == 'constchar*' or paramNoSpaces == 'charconst*':
                self.file.write('    char ' + parameter.name + '[MAX_NR_FUNCTION_CALLS][MAX_STRING_LENGTH];\n')
            else:
                paramType = parameter.type.replace('const', '')
                while paramType.find('  ') >= 0:
                    paramType = paramType.replace('  ', ' ')
                paramType = paramType.replace('*', '').strip()
                self.file.write('    ' + paramType + ' ' + parameter.name + '[MAX_NR_FUNCTION_CALLS];\n')

    def writePrototypesToHeaderfile(self, mockinfo):
        self.headerfile = self.headerfile[:self.headerfile.rfind('.')]
        self.file.write('void ' + self.headerfile + '_MockSetup(void);    /* call this before every test! */\n')
        self.file.write('void ' + self.headerfile + '_MockTeardown(void); /* call this after every test! */\n\n')
        self.file.write('/* call these for each call you expect for a given function */')
        for mock in mockinfo:
            prototype = '\n' + self.makePrototype(mock) + ';'
            self.file.write(prototype)


################################################################################

class SourceGenerator(FileGenerator):
    def __init__(self, headerfile, maxNrFunctionCalls):
        super(SourceGenerator, self).__init__(headerfile, '.c', maxNrFunctionCalls)

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
        self.file.write('#include <string.h>\n')
        self.file.write(UNITY_INCLUDE + '\n')
        self.file.write('#include "' + self.file.createMockName('.h') + '"\n')
        for custom_include in CUSTOM_INCLUDES:
            self.file.write(custom_include + '\n')
        self.file.write('\n')

    def writeDefinesAndGlobalVarsToSourceFile(self, mockinfo):
        self.file.write('#define MAX_LENGTH_ERROR_MESSAGE 100\n\n')
        for mock in mockinfo:
            self.file.write('static ' + mock.functionName + 'Struct ' + mock.functionName + 'Data;\n')
        self.file.write('\n')

    def writeSetupAndTearDownToSourceFile(self, mockinfo):
        function = self.headerfile[:self.headerfile.rfind('.')]
        self.file.write('void ' + function + '_MockSetup(void)\n')
        self.file.write('{\n')
        for mock in mockinfo:
            initline = '    memset(&' + mock.functionName + 'Data, 0, sizeof(' + mock.functionName + 'Data));\n'
            self.file.write(initline)
        self.file.write('}\n\n')

        self.file.write('void ' + function + '_MockTeardown(void)\n')
        self.file.write('{\n')
        for mock in mockinfo:
            assertline =  '    TEST_ASSERT_EQUAL_MESSAGE(' + mock.functionName + 'Data.ExpectedNrCalls,\n'
            assertline += '                              ' + mock.functionName + 'Data.CallCounter,\n'
            assertline += '                              "' + mock.functionName + ' was not called as often as specified!");\n'
            self.file.write(assertline)
        self.file.write('}')

    def writeExpectedCallFunction(self, mock):
        prototype = '\n\n\n' + self.makePrototype(mock) + '\n'
        self.file.write(prototype)
        self.file.write('{\n')
        self.file.write('    char errormsg[MAX_LENGTH_ERROR_MESSAGE];\n')
        self.file.write('    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s, max number is: %d", __FUNCTION__, MAX_NR_FUNCTION_CALLS);\n')
        self.file.write('    TEST_ASSERT_TRUE_MESSAGE(' + mock.functionName + 'Data.ExpectedNrCalls < MAX_NR_FUNCTION_CALLS, errormsg);\n')
        self.writeNullTestsToSourceFile(mock)
        self.file.write('\n')
        self.writeParameterCopyLinesToSourceFile(mock)
        self.writeReturnTypeCopyLinesToSourceFile(mock)
        self.file.write('    ' + mock.functionName + 'Data.ExpectedNrCalls++;\n')
        self.file.write('}\n\n')

    def writeNullTestsToSourceFile(self, mock):
        for parameter in mock.parameters:
            if parameter.type.find('*') >= 0:
                self.file.write('    TEST_ASSERT_NOT_NULL_MESSAGE(' + parameter.name + ', "parameter should not be NULL");\n')
        if mock.returnType.find('*') >= 0:
            self.file.write('    /* no TEST_ASSERT_NOT_NULL for ReturnValue, you might want to return NULL! */\n')

    def writeParameterCopyLinesToSourceFile(self, mock):
        for parameter in mock.parameters:
            paramNoSpaces = parameter.type.replace(' ', '')
            paramNoConst = self.removeConstFromType(parameter.type)
            if paramNoSpaces == 'constchar*' or paramNoSpaces == 'charconst*':
                self.file.write('    strncpy(' + mock.functionName + 'Data.' + parameter.name + '[' + mock.functionName + 'Data.ExpectedNrCalls], ' + parameter.name + ', MAX_STRING_LENGTH);\n')
            elif paramNoConst.find('*') >= 0:
                self.file.write('    ' + mock.functionName + 'Data.' + parameter.name + '[' + mock.functionName + 'Data.ExpectedNrCalls] = *' + parameter.name + ';\n')
            elif paramNoConst.strip() != 'void':
                self.file.write('    ' + mock.functionName + 'Data.' + parameter.name + '[' + mock.functionName + 'Data.ExpectedNrCalls] = ' + parameter.name + ';\n')

    def writeReturnTypeCopyLinesToSourceFile(self, mock):
        if mock.returnType != 'void':
            self.file.write('    ' + mock.functionName + 'Data.ReturnValue[' + mock.functionName + 'Data.ExpectedNrCalls] = ReturnValue;\n')

    def writeMockFunction(self, mock):
        prototype = mock.returnType + ' ' + mock.functionName + '('
        for parameter in mock.parameters:
            prototype += parameter.original + ', '
        # strip last ', '
        if prototype[-2:] == ', ':
            prototype = prototype[:-2]
        prototype += ')\n'
        self.file.write(prototype)    
        self.file.write('{\n')
        self.file.write('    char errormsg[MAX_LENGTH_ERROR_MESSAGE];\n\n')
        self.file.write('    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Too many calls to %s: expected %d calls, this is call nr %d", __FUNCTION__, ' + mock.functionName + 'Data.ExpectedNrCalls, ' + mock.functionName + 'Data.CallCounter+1);\n')
        self.file.write('    TEST_ASSERT_TRUE_MESSAGE(' + mock.functionName + 'Data.CallCounter < ' + mock.functionName + 'Data.ExpectedNrCalls, errormsg);\n')
        self.file.write('\n')
        self.writeParameterLinesToMockFunction(mock)
        if mock.returnType == 'void':
            self.file.write('    ' + mock.functionName + 'Data.CallCounter++;\n')
        else:
            self.file.write('    return ' + mock.functionName + 'Data.ReturnValue[' + mock.functionName + 'Data.CallCounter++];\n')
        self.file.write('}')

    def writeParameterLinesToMockFunction(self, mock):
        if not self.isVoidParameter(mock.parameters):
            self.file.write('    snprintf(errormsg, MAX_LENGTH_ERROR_MESSAGE, "Call to %s with unexpected parameter(s) in call nr %d", __FUNCTION__, ' + mock.functionName + 'Data.CallCounter+1);\n')
            for parameter in mock.parameters:
                if parameter.type.find('*') >= 0 and parameter.type.find('const') == -1:
                    # output parameter: copy expected data into parameter
                    # if parameter.type.replace(' ', '') == 'char*':
                    #     self.file.write('        strncpy(' + parameter.name + ', ' + mock[0] + 'Data.' + parameter.name + '[' + mock[0] + 'Data.CallCounter], MAX_STRING_LENGTH);\n')
                    # else:
                    self.file.write('    *' + parameter.name + ' = ' + mock.functionName + 'Data.' + parameter.name + '[' + mock.functionName + 'Data.CallCounter];\n')
                else:
                    # input parameter: check if expected data is correct
                    paramNoSpaces = parameter.type.replace(' ', '')
                    if paramNoSpaces == 'constchar*' or paramNoSpaces == 'charconst*':
                        self.file.write('    TEST_ASSERT_EQUAL_STRING_MESSAGE(' + mock.functionName + 'Data.' + parameter.name + '[' + mock.functionName + 'Data.CallCounter], ' + parameter.name + ', errormsg);\n')
                    elif parameter.type.find('*') >= 0:
                        typeWithoutConstOrPtr = parameter.type.replace('const', '').replace('*', '').strip()
                        unityTesttype = self.findUnityTestType(typeWithoutConstOrPtr)
                        if unityTesttype == None:
                            self.file.write('    TEST_ASSERT_EQUAL_MEMORY_MESSAGE(&(' + mock.functionName + 'Data.' + parameter.name + '[' + mock.functionName + 'Data.CallCounter]), ' + parameter.name + ', sizeof(*' + parameter.name + '), errormsg);\n')
                        else:
                            self.file.write('    ' + unityTesttype + '(' + mock.functionName + 'Data.' + parameter.name + '[' + mock.functionName + 'Data.CallCounter], *' + parameter.name + ', errormsg);\n')
                    else:
                        unityTesttype = self.findUnityTestType(parameter.type)
                        if unityTesttype == None:
                            self.file.write('    TEST_ASSERT_EQUAL_MEMORY_MESSAGE(&(' + mock.functionName + 'Data.' + parameter.name + '[' + mock.functionName + 'Data.CallCounter]), &' + parameter.name + ', sizeof(' + parameter.name + '), errormsg);\n')
                        else:
                            self.file.write('    ' + unityTesttype + '(' + mock.functionName + 'Data.' + parameter.name + '[' + mock.functionName + 'Data.CallCounter], ' + parameter.name + ', errormsg);\n')

    def findUnityTestType(self, paramType):
        global CTYPE_TO_UNITY_ASSERT_MACRO
        for ctype in CTYPE_TO_UNITY_ASSERT_MACRO:
            if ctype[0] == paramType:
                return ctype[1]
        return None

################################################################################
################### OTHER STUFF ################################################
################################################################################

################################## usage/exit ##################################
def makeDescription():
    global DESCRIPTION
    global VERSION
    return DESCRIPTION + ', version: ' + VERSION

def printVersionAndExit():
    global DESCRIPTION
    global VERSION
    global AUTHOR
    global LICENSE
    print(makeDescription())
    print('Copyright (C) 2015 ' + AUTHOR)
    print('License: ' + LICENSE)
    print('This is free software; see the source for copying conditions.  There is NO')
    print('warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n')
    sys.exit()

def printUsageAndExit():
    global DESCRIPTION
    global VERSION
    printerror([makeDescription(), "\n\n" \
               'Error: wrong (number of) parameters, please use:\n', \
               sys.argv[0], ' [options] header.h\n', \
               '  options: -n#: max number of expected function calls per function (default: 25)\n', \
               '           -v : verbose mode\n' \
               '     --version: version information'])

################################# main function ################################
def main():
    global Verbose
    global MaxNrFunctionCalls
    headerfile = ''

    for arg in sys.argv[1:]:
        if arg[:1] != '-':
            headerfile = arg
        elif arg[:2] == '-n':
            MaxNrFunctionCalls = arg[2:]
        elif arg[:2] == '-v':
            Verbose = True
        elif arg == '--version':
            printVersionAndExit()
        else:
            printUsageAndExit()

    if headerfile == '':
        printUsageAndExit()

    proto = Prototypes(headerfile)

    if proto.anyPrototypesFound():
        mockinfo = proto.getMockInfo()
        printMockInfo(mockinfo)

        hgen = HeaderGenerator(headerfile, MaxNrFunctionCalls)
        hgen.generate(mockinfo)
        cgen = SourceGenerator(headerfile, MaxNrFunctionCalls)
        cgen.generate(mockinfo)


if __name__ == '__main__':
    sys.exit(main())
