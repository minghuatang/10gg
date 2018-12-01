import time
from datetime import datetime, timedelta
import requests
import json
from settings import site_settings

HTTP_PREFIX = "http://"
PROMETHEUS_HOST = site_settings['prometheus_host'] 
PROMETHEUS_PORT = site_settings['prometheus_port']
PROMETHEUS_ADDR = HTTP_PREFIX + PROMETHEUS_HOST + ":" + PROMETHEUS_PORT
RANGE_QUERY_API = "/api/v1/query_range"

def query(query, start_time, end_time):
    data_set = dict()
    addr = PROMETHEUS_ADDR + RANGE_QUERY_API
    response = requests.get(addr,
                            params={'query': query, 'start': start_time,
                                     'end': end_time, 'step': 60})
    return response.json()

if __name__ == "__main__":
    tq = r'sum(delta(pd_schedule_operators_count{instance="192.168.199.118:2379", event="create"}[1m]))'

    tq2 = "pd_schedule_operators_count"
    start = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = (datetime.now() - timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%SZ")
    query(tq,start,end)

