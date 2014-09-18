__author__ = 'talbarda'
import random
import uuid
from src.sensor.http_client import http_client
from src.utilities.utils import get_conf, get_current_time
import time

INTERVAL = get_conf().get_conf_value(full_name="sensor.update_seconds_interval", val_type=float, def_val=1)

def collect_data():
    return dict(ts=str(get_current_time()),
                uid=str(uuid.uuid1()),
                temparture=-5 + (45*random.random()),
                pressure=300 + (400*random.random()))

if __name__ == "__main__":

    with http_client()  as client:
        while True:
            print client.send_data(data_dict=collect_data())
            time.sleep(INTERVAL)


