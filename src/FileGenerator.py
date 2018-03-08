from FileWriter import *


class FileGenerator(object):
    def __init__(self, headerfile, extension, maxNrFunctionCalls, version):
        self.headerfile = self.getBasename(headerfile)
        self.file = FileWriter(
            self.headerfile, extension, maxNrFunctionCalls, version)

    def getBasename(self, path):
        path = path.replace('\\', '/').rstrip('/')
        return path[path.rfind('/') + 1:]

    def removeConstFromType(self, ctype):
        ctype = ctype.replace('const', '').strip()
        while ctype.find('  ') >= 0:
            ctype = ctype.replace('  ', ' ')
        return ctype

    def makeExpectedCallPrototype(self, mock, lineEnding):
        prototype = 'void ' + mock.functionName + '_ExpectedCall('
        # parameters
        funcptrParameterFound = False
        if (self.isVoidParameter(mock.parameters)) and \
                (mock.returnType == 'void'):
            prototype += 'void'
        elif (not self.isVoidParameter(mock.parameters)):
            for parameter in mock.parameters:
                if parameter.funcptr:
                    funcptrParameterFound = True
                param = parameter.original
                if (not parameter.funcptr) and (param.find('*') >= 0) and \
                        (param.find('const') < 0):
                    param = 'const ' + param
                prototype += param + ', '
        # return value
        if mock.returnType != 'void':
            prototype += self.removeConstFromType(
                mock.returnType) + ' ReturnValue'
        # strip last ', '
        if prototype[-2:] == ', ':
            prototype = prototype[:-2]

        prototype += ')' + lineEnding
        if funcptrParameterFound:
            prototype += ' /* if you don\'t want to check function ' \
                'pointer(s), make it NULL */'
        return prototype

    def isVoidParameter(self, parameterlist):
        return (len(parameterlist) == 1) and (parameterlist[0].type == 'void')
