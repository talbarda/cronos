import json
import sys

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
temperature_sensor = grove.GroveTemp(0)
pressure_sensor = mraa.Aio(2)
light = mraa.Gpio(2)
light.dir(mraa.DIR_OUT)
light_value = 0
light.write(light_value)

def change_light(val):
    global light_value
    if light_value!=val:
        light_value=val
        light.write(val)

def collect_data():
    return dict(ts=str(get_current_time()),
                uid=str(uuid.uuid1()),
                temperature=get_temp(),
                pressure=get_pressure())

def get_temp():
    a = temperature_sensor.raw_value()
    a = int(a) >> 2
    r = float((1023-a)*10000/a)
    return 1.7*(1/(math.log(r/10000)/3975 + 1/298.15)-273.15)

def get_pressure():
    return pressure_sensor.read()

def handle_response(response_val):
    response_dict = json.loads(response_val)
    if response_dict["temperature"]>=20:
        change_light(1)
    else:
        change_light(0)
    print response_val

if __name__ == "__main__":

    while True:
        try:
            with http_client() as client:
                while client.is_opened:
                    handle_response(client.send_data(data_dict=collect_data()))
                    time.sleep(INTERVAL)
        except:
            print sys.exc_info()


