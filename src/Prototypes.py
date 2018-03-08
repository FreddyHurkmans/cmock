import subprocess
from configuration import CTAGS_EXECUTABLE


class MockInfoStruct:
    # MockInfo is used as a struct, it will contain:
    # field          type
    # ------------------------
    # .functionName  string
    # .returnType    string
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


class Prototypes(object):
    def __init__(self, headerfile):
        self.headerfile = headerfile
        self.getPrototypesUsingCtags()

    def getPrototypesUsingCtags(self):
        global CTAGS_EXECUTABLE
        self.ctagsOutput = str(subprocess.check_output(
            [CTAGS_EXECUTABLE, '-x', '-u', '--c-kinds=fp', self.headerfile]))
        self.ctagsOutput = self.ctagsOutput.split('\\n')
        self.ctagsOutput = self.ctagsOutput[:-1]

    def anyPrototypesFound(self):
        return len(self.ctagsOutput) > 0

    def getMockInfo(self):
        mockinfo = []
        for prototype in self.ctagsOutput:
            prototype = prototype[prototype.find(self.headerfile) +
                                  len(self.headerfile) + 1:].strip()
            prototype = self.removeExternKeyword(prototype)
            leftPart = prototype[:prototype.find('(')]

            mock = MockInfoStruct()
            (mock.functionName, mock.returnType,
             mock.funcptr) = self.splitParameterTypeAndName(leftPart)
            parameterList = self.splitParameterList(prototype)
            mock.parameters = []
            for parameter in parameterList:
                paraminfo = ParamInfoStruct()
                paraminfo.original = parameter.strip()
                (paraminfo.name, paraminfo.type, paraminfo.funcptr) = \
                    self.splitParameterTypeAndName(paraminfo.original)
                mock.parameters.append(paraminfo)
            mockinfo.append(mock)
        return mockinfo

    def removeExternKeyword(self, prototype):
        if prototype.find('extern') == 0:
            prototype = prototype[6:].strip()
        return prototype

    def splitParameterTypeAndName(self, parameter):
        funcPtr = False
        if parameter.strip() == 'void':
            paramName = ''
            paramType = 'void'
        elif parameter.find('(') >= 0:
            # function pointer
            funcPtr = True
            # int **(*callback)(int** p)
            paramName = parameter[parameter.find('(') + 1:
                                  parameter.find(')')].strip('*')
            paramType = ''
        else:
            lastSpace = parameter.rfind(' ')
            lastStar = parameter.rfind('*')
            paramName = parameter[max(lastSpace, lastStar) + 1:].strip()
            paramType = parameter[:parameter.rfind(paramName)].strip()
        return [paramName, paramType, funcPtr]

    def splitParameterList(self, prototype):
        prototype = prototype[prototype.find('(') + 1:
                              prototype.rfind(')')].strip()
        parameterList = []
        # functionPointer builds functionpointer parameter, can be split over
        # multiple parameters due to split on comma!
        functionPointer = ''
        # functionPointerBracketCount remembers the number of brackets in
        # functionptr that are still open (should become 0 at end of
        # functionptr)
        functionPointerBracketCount = 0
        for parameter in prototype.split(','):
            if functionPointerBracketCount == 0 and parameter.count('(') == 0:
                # no function pointer
                parameterList.append(parameter)
            else:
                # part of function pointer
                functionPointerBracketCount += parameter.count(
                    '(') - parameter.count(')')
                functionPointer += parameter + ','
                if functionPointerBracketCount == 0:
                    parameterList.append(functionPointer[:-1])
                    functionPointer = ''
        return parameterList

        parameterList = prototype.split(',')
        return parameterList
