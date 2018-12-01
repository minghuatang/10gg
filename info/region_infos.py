import requests
import json

HTTP_PREFIX = "http://"
PD_HOST = "172.16.30.38"
PD_PORT = "13379"
TIDB_HOST = "172.16.30.38"
TIDB_PORT = "10083"
PD_REGION_PREFIX = "/pd/api/v1/region/id/"
TABLE_PREFIX  = "/tables/"
TIDB_REGION_SUFFIX = "/regions"
SCHEMA_ROOT_PREFIX = "/schema/"

def region_infos(id):
    pd_request = HTTP_PREFIX + PD_HOST + ":" + PD_PORT + PD_REGION_PREFIX + "%d" % (id)
    pd_res = requests.get(pd_request)
    data_pd = pd_res.json()
    
    tidb_request = HTTP_PREFIX+ TIDB_HOST + ":" + TIDB_PORT + TIDB_REGION_SUFFIX + "/" + "%d" % (id)
    tidb_res = requests.get(tidb_request)
    data_tidb = tidb_res.json()
    frames = data_tidb['frames']
    l = []
    for frame in frames:
        db_name = frame['db_name']
        table_name = frame['table_name']
        table_request = HTTP_PREFIX + TIDB_HOST + ":" + TIDB_PORT + TABLE_PREFIX + str(db_name) + "/" + str(table_name) + TIDB_REGION_SUFFIX
        table_res = requests.get(table_request)
        data_table = table_res.json()
        schema_request = HTTP_PREFIX + TIDB_HOST + ":" + TIDB_PORT + SCHEMA_ROOT_PREFIX + str(db_name) + "/" + str(table_name)
        schema_res = requests.get(schema_request)
        data_schema = schema_res.json()
        data_schema['record_regions'] = data_table['record_regions']
        l.append(data_schema)

    out = data_pd
    out['table_info'] = l
    out['start_key'] = data_tidb['start_key']
    out['end_key'] = data_tidb['end_key']
    out['frames'] = data_tidb['frames']
