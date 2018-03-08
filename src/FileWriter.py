from time import strftime


class FileWriter(object):
    def __init__(self, sourcefilename, extension, maxNrFunctionCalls, version):
        self.sourcefilename = sourcefilename
        self.filename = self.createMockName(extension)
        self.maxNrFunctionCalls = maxNrFunctionCalls
        self.version = version
        self.fd = open(self.filename, 'w')
        self.writeHeader()

    def __del__(self):
        self.writeFooter()
        self.fd.close()

    def createMockName(self, extension):
        return self.sourcefilename[:self.sourcefilename.rfind('.')] + \
            '_mock' + extension

    def writeHeader(self):
        self.writeGenericHeader()
        if self.filename[-2:] == '.h':
            self.writeHeaderfileExtras()

    def writeGenericHeader(self):
        self.fd.write('/' + '*' * 79 + '\n')
        self.fd.write(' * generated code, please do not edit directly\n')
        self.fd.write(' * cMock version ' + self.version +
                      ' written by Freddy Hurkmans\n')
        self.fd.write(' *\n')
        self.fd.write(' * source file    : ' + self.sourcefilename + '\n')
        self.fd.write(' * filename       : ' + self.filename + '\n')
        self.fd.write(' * generation date: ' +
                      strftime('%d %b %Y - %H:%M:%S') + '\n')
        self.fd.write(' *\n')
        self.fd.write(' ' + '*' * 78 + '/\n\n')

    def writeHeaderfileExtras(self):
        defineName = self.headerProtectionDefine()
        self.fd.write('#ifndef ' + defineName + '\n')
        self.fd.write('#define ' + defineName + '\n\n')
        self.fd.write('#include "' + self.sourcefilename + '"\n\n')
        self.writeSystemIncludes()
        self.fd.write('#define MAX_NR_FUNCTION_CALLS ' +
                      self.maxNrFunctionCalls + '\n\n')

    def headerProtectionDefine(self):
        return self.filename.upper().replace('.', '_')

    def writeSystemIncludes(self):
        self.fd.write('#include <stdbool.h>\n')
        self.fd.write('#include <stdint.h>\n\n')

    def writeFooter(self):
        if self.filename[-2:] == '.h':
            self.fd.write('\n\n#endif  /* ' +
                          self.headerProtectionDefine() + ' */')
        self.fd.write('\n')

    def write(self, line):
        self.fd.write(line)
