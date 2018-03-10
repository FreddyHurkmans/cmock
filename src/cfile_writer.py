from configuration import Config
from time import strftime


class CFileWriter(object):
    def __init__(self, input_header, extension):
        self.input_header = self.__get_basename(input_header)
        self.basename = self.__strip_extension(self.input_header)
        self.filename = self.create_mock_name(extension)
        self.__fd = open(self.filename, 'w')
        self.__write_header()

    def __del__(self):
        self.__write_footer()
        self.__fd.close()

    def write(self, line):
        self.__fd.write(line)

    def create_mock_name(self, extension):
        return self.basename + '_mock' + extension

    def __get_basename(self, path):
        # strip path info
        path = path.replace('\\', '/').rstrip('/')
        return path[path.rfind('/') + 1:]

    def __strip_extension(self, path):
        return path[:path.rfind('.')]

    def __write_header(self):
        self.__write_generic_header()

    def __write_generic_header(self):
        self.__fd.write('/' + '*' * 79 + '\n')
        self.__fd.write(' * generated code, please do not edit directly\n')
        self.__fd.write(' * cMock version ' + Config.VERSION +
                        ' written by Freddy Hurkmans\n')
        self.__fd.write(' *\n')
        self.__fd.write(' * source file    : ' + self.input_header + '\n')
        self.__fd.write(' * filename       : ' + self.filename + '\n')
        self.__fd.write(' * generation date: ' +
                        strftime('%d %b %Y - %H:%M:%S') + '\n')
        self.__fd.write(' *\n')
        self.__fd.write(' ' + '*' * 78 + '/\n\n')

    def __write_footer(self):
        # files should end with a newline in Unix
        self.__fd.write('\n')
