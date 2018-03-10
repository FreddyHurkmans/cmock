from configuration import Config


class Type(object):
    @staticmethod
    def is_string(param_no_spaces):
        return param_no_spaces in ['constchar*', 'charconst*'] or \
            (Config.charstar_is_input_string and param_no_spaces == 'char*')

    @staticmethod
    def is_output_pointer(param_type):
        return Type.is_pointer(param_type) and param_type.find('const') == -1

    @staticmethod
    def is_pointer(param_type):
        return param_type.find('*') >= 0

    @staticmethod
    def is_void(param_type):
        return param_type.strip() == 'void'
