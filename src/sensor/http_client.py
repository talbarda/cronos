from src.utilities.utils import get_conf

__author__ = 'talbarda'

import httplib
import json

CONF_SECTION = "http_server"
conf = get_conf()
DEF_HOST = conf.get_conf_value(full_name="%s.host" % CONF_SECTION, val_type=str, def_val="localhost")
DEF_METHOD = conf.get_conf_value(full_name="%s.method" % CONF_SECTION, val_type=str, def_val="GET")
DEF_PORT = conf.get_conf_value(full_name="%s.port" % CONF_SECTION, val_type=int, def_val=8080)
DEF_TIMEOUT = get_conf().get_conf_value(full_name="%s.timeout" % CONF_SECTION, val_type=int, def_val=10)


class http_client(object):
    def __init__(self, host=DEF_HOST, method=DEF_METHOD, port=DEF_PORT, timeout=DEF_METHOD):
        self.http_conn = httplib.HTTPConnection(host, port, timeout)
        self.is_opened = True
        self.request_method = method
        self.headers = {"content-type": 'application/json'}

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        try:
            if self.is_opened:
                self.http_conn.close()
                self.is_opened = False
            print "closed"
        except:
            pass


    def send_data(self, data_dict, wait_for_response=True, relative_url=""):
        data_to_send = json.dumps(data_dict)

        self.http_conn.request(method=self.request_method,
                               url=relative_url,
                               body=data_to_send,
                               headers=self.headers)

        response = None
        if wait_for_response:
            response = self.http_conn.getresponse().read().decode()

        return response





