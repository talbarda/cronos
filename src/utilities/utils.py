from datetime import datetime
from src.utilities.config_handler import config_handler

__author__ = 'talbarda'

GLOBAL_CONFIG_VAR_NAME = "conf"

def get_conf():
    global conf
    if GLOBAL_CONFIG_VAR_NAME not in globals():
        conf = config_handler(config_file_path="../../conf/conf.cfg")
    return conf

def get_current_time():
    return datetime.now()

if __name__ == "__main__":
    print get_conf().get_conf_value("http_server.host")
