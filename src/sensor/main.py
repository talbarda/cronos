__author__ = 'talbarda'

from src.sensor.http_client import http_client
from src.utilities.utils import get_conf
import time

INTERVAL = get_conf().get_conf_value(full_name="sensor.update_seconds_interval", val_type=float, def_val=1)

def collect_data():
    return dict()

if __name__ == "__main__":

    with http_client()  as client:
        while True:
            client.send_data(data_dict=collect_data())
            time.sleep(INTERVAL)


