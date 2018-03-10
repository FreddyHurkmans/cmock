#!/usr/bin/python3

import sys
from configuration import *
from prototype_finder import PrototypeFinder
from headergen import HeaderGenerator
from sourcegen import SourceGenerator


# NOTES:
# This is a rather straight forward mock generator with the following
# limitations:
# - it depends on ctags to read function prototypes from the given
#   headerfile
# - array parameters are NOT SUPPORTED
# - pointers to pointers are NOT SUPPORTED
# - const pointer parameters (e.g. const MYTYPE*) are considered to be input
#   parameters, const char* types are considered to be input strings
# - pointer parameters (e.g. MYTYPE*) are considered to be output parameters,
#   char* types are considered to be output chars, thus no string (remember:
#   arrays are not supported!)
#
# for mock generation, this means that:
# int foo(const MYTYPE* bar);
# will generate a mock foo function and a function to indicate expected calls:
# void foo_ExpectedCall(const MYTYPE* bar, int ReturnValue)
# In this case: bar is a const pointer type. Thus it is considered to be an
# input parameter. In the ExpectedCall function bar is copied into local
# memory of type MYTYPE and in the mock foo function, bar is checked against
# the expected value.
#
# THE OTHER CASE:
# int foo(MYTYPE* bar);
# will also generate a mock foo function and a function to indicate expected
# calls:
# void foo_ExpectedCall(const MYTYPE* bar, int ReturnValue)
# In this case: bar is a non-const pointer type. Thus it is considered to be
# an output parameter. In the ExpectedCall function bar is copied into local
# memory of type MYTYPE and in the mock foo function, the copied bar data is
# copied into the dereferenced bar parameter.


# ################## PRINT METHODS ###########################################
def printf(line):
    # prints to stdout if verbose is set
    if verbose:
        print(line)


def print_mock_info(mockinfo):
    printf('FUNCTION\t\tRETURN TYPE\t\tPARAMETER LIST')
    for mock in mockinfo:
        line = mock.function_name + '\t\t' + mock.return_type + '\t\t'
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


# ################################# usage/exit ###############################
def make_description():
    return DESCRIPTION + ', version: ' + VERSION


def print_version_and_exit():
    print(make_description())
    print('Copyright (C) 2018 ' + AUTHOR)
    print('License: ' + LICENSE)
    print('This is free software; see the source for copying conditions.')
    print('There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR')
    print('A PARTICULAR PURPOSE.\n')
    sys.exit()


def print_usage_and_exit():
    printerror(
        [make_description(), "\n\n"
            'Error: wrong (number of) parameters, please use:\n',
            sys.argv[0], ' [options] header.h\n',
            '  options: -n#: max number of expected function calls per '
            'function (default: 25)\n',
            '           -v : verbose mode\n'
            '     --version: version information'])


# ############################## main function ###############################
def main():
    global max_nr_function_calls
    global verbose
    headerfile = ''

    for arg in sys.argv[1:]:
        if arg[:1] != '-':
            headerfile = arg
        elif arg[:2] == '-n':
            max_nr_function_calls = arg[2:]
        elif arg[:2] == '-v':
            verbose = True
        elif arg == '--version':
            print_version_and_exit()
        else:
            print_usage_and_exit()

    if headerfile == '':
        print_usage_and_exit()

    proto = PrototypeFinder(headerfile)

    if proto.any_prototypes_found():
        mockinfo = proto.get_mock_info()
        print_mock_info(mockinfo)

        hgen = HeaderGenerator(headerfile, max_nr_function_calls, VERSION)
        hgen.generate(mockinfo)
        cgen = SourceGenerator(headerfile, max_nr_function_calls, VERSION)
        cgen.generate(mockinfo)


if __name__ == '__main__':
    sys.exit(main())
