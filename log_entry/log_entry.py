#!/usr/bin/env python3

# 如何在内存里表示一条log


SOURCE_TIDB = 0
SOURCE_TIKV = 1
SOURCE_METRIC = 2
SOURCE_OS = 3

sample_tidb_log_entry = {
    'source': SOURCE_TIDB,
    'log_time': '2018/11/30 13:24:05.143',
    'log_level': 'INFO',
    'file_name': 'tikv-server.rs',
    'file_line': 398,
    'content': '', # 剩下的全部内容
    'region': 11, # optional
    'store': 1, # optional
}

# 如何抽取一部分 log, 大概的接口，具体实现再议
# 1. 传入filters，按自定义的filter函数过滤
# 2. 传入字段名称，自己判断
def filter_log_entries(log_entries, **kw):

    filters = kw['filters']
    res = log_entries
    for f in filters:
        res = filter(log_entries, f)

    region = kw['region']
    res = filter(log_entries, lambda log : 'region' in log and log['region'] == region)

    return res
