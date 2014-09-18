__author__ = 'talbarda'
import os
import ConfigParser

GENERAL_CONF_SECTION_NAME = "GENERAL"



class config_handler(object):
    def __init__(self, config_file_path=None):
        config_file_path = os.path.realpath(config_file_path)
        if not os.path.exists(config_file_path):
            raise IOError
        self.config = ConfigParser.ConfigParser()
        self.read_config(config_file_path)

    def read_config(self, configFileName):
        self.config.read([configFileName])

    def get_all_in_section_as_dictionary(self, section_name):
        return dict(self.config.items(section_name))

    def get_conf_value(self, full_name, val_type=str,
                       def_val=None):
        param_full_name_lowered = full_name
        param_parts = param_full_name_lowered.split(".")

        # # Checking if the param asked is the "param_name" format that means it is in the general parameters
        # # or in "Section.param_name" format"
        if len(param_parts) == 1:
            param_section = GENERAL_CONF_SECTION_NAME
        else:
            param_section = param_parts[0]

        param_name = param_parts[len(param_parts) - 1]

        try:
            if val_type is int:
                param_value = self.config.getint(param_section, param_name)
            elif val_type is float:
                param_value = self.config.getfloat(param_section, param_name)
            elif val_type is bool:
                param_value = self.config.getboolean(param_section, param_name)
            else:
                param_value = self.config.get(param_section, param_name)
                if not val_type is str:
                    param_value = val_type(param_value)

            return param_value
        except ConfigParser.NoSectionError:
            return def_val
        except ConfigParser.NoOptionError:
            return def_val