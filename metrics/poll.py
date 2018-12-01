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

CPU_Metrics = {
    'raft_store_cpu' : r'sum(rate(tikv_thread_cpu_seconds_total{name=~"raftstore_.*"}[1m])) by (job, name)',
    'async_apply_cpu' : r'sum(rate(tikv_thread_cpu_seconds_total{name=~"apply_worker"}[1m])) by (job)',
    'local_read_cpu' : r'sum(rate(tikv_thread_cpu_seconds_total{name=~"local_reader"}[1m])) by (job, name)',
    'scheduler_cpu' : r'sum(rate(tikv_thread_cpu_seconds_total{name=~"storage_schedul.*"}[1m])) by (job)',
    'storage_read_pool_cpu': r'sum(rate(tikv_thread_cpu_seconds_total{name=~"store_read.*"}[1m])) by (job)',
    'coprocessor_cpu': r'sum(rate(tikv_thread_cpu_seconds_total{name=~"cop_.*"}[1m])) by (job)',
    'snapshot_worker_cpu':r'sum(rate(tikv_thread_cpu_seconds_total{name=~"snapshot_worker"}[1m])) by (job)',
    'rockdb_cpu': r'sum(rate(tikv_thread_cpu_seconds_total{name=~"rocksdb.*"}[1m])) by (job)',
    'grpc_cpu': r'sum(rate(tikv_thread_cpu_seconds_total{name=~"grpc.*"}[1m])) by (job)',
}

def query(query, start_time, end_time):
    addr = PROMETHEUS_ADDR+ ":" + str(PROMETHEUS_PORT) + RANGE_QUERY_API
    response = requests.get(addr,
                            params={'query': query, 'start': start_time,
                                     'end': end_time, 'step': 15})
    return response.json()

if __name__ == "__main__":
    addr = "172.16.30.38:13379"
    # tq = r'sum(delta(pd_schedule_operators_count{{instance="{}", event="create"}}[1m]))'.format(addr)
    # tq = CPU_Metrics['async_apply_cpu']
    start = (datetime.utcnow() - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = (datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%SZ")
    for v in CPU_Metrics.values():
        tq = v
        r = query(tq,start,end)
        print(r)
