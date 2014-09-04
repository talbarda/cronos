__author__ = 'talbarda'
import random
import uuid
from src.sensor.http_client import http_client
from src.utilities.utils import get_conf, get_current_time
import time
import mraa
import pyupm_grove as grove
import math

INTERVAL = get_conf().get_conf_value(full_name="sensor.update_seconds_interval", val_type=float, def_val=1)

def collect_data():
    return dict(ts=str(get_current_time()),
                uid=str(uuid.uuid1()),
                temparture=get_temp(),
                pressure=get_pressure())

def get_temp():
    x = grove.GroveTemp(0)
    a = x.raw_value()
    a = int(a) >> 2
    r = float((1023-a)*10000/a)
    return 1.7*(1/(math.log(r/10000)/3975 + 1/298.15)-273.15)

def get_pressure():
    x = mraa.Aio(2)
    return x.read()

def handle_response(response_val):
    print response_val

if __name__ == "__main__":

    with http_client()  as client:
        while True:
            handle_response(client.send_data(data_dict=collect_data()))
            time.sleep(INTERVAL)


