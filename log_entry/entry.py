#!/usr/bin/env python3

import re

SOURCE_TIDB = 'TIDB'
SOURCE_TIKV = 'TIKV'
SOURCE_PD = 'PD'

SOURCE_METRIC = 'METRIC'
SOURCE_OS = 'OS'

LOG_DEBUG = 0
LOG_INFO = 1
LOG_WARN = 2
LOG_ERROR = 3
LOG_FATAL = 4
LOG_NULL = 5

# 因为map结构没有固定schema，我们可以针对一种log类型做任意扩展

sample_tikv_log_entry = {
    'source': SOURCE_TIKV,
    'log_time': '2018/11/30 13:24:05.143',
    'log_level': 'INFO',
    'file_name': 'tikv-server.rs',
    'file_line': 398,
    'content': '', # 剩下的全部内容
    'region': 11, # optional
    'store': 1, # optional
    'tags': ['store', 'region'] # optional
}

sample_tidb_log_entry = {
    'source': SOURCE_TIDB,
    'log_time': '2018/11/30 13:24:08.601',
    'log_level': 'info',
    'file_name': 'client.go',
    'file_line': 398,
    'content': '', # 剩下的全部内容
    'tags': ['SLOW_QUERY', 'INTERNAL'] # optional
}

sample_pd_log_entry = {
    'source': SOURCE_PD,
    'log_time': '2018/11/30 13:24:08.601',
    'log_level': 'info',
    'file_name': 'cluster_info.go',
    'file_line': 398,
    'content': '', # 剩下的全部内容
    'region': 12, # optional
    'tags': ['SLOW_QUERY', 'INTERNAL'] # optional
}

def filter_by_datetime(log_entries, begin, end):
    return filter(lambda e : begin <= e['log_time'][:-4] and e['log_time'][:-4] < end, log_entries)

def filter_by_date(log_entries, begin, end):
    return filter(lambda e : begin <= e['log_time'][:10] and e['log_time'][:10] < end, log_entries)

def filter_by_level(log_entries, level):
    return filter(lambda e : e['log_level'] >= level, log_entries)

def filter_by_filename(log_entries, filename):
    return filter(lambda e : e['file_name'] == filename, log_entries)

def filter_by_tag(log_entries, tag):
    return filter(lambda e : tag in e['tags'], log_entries)

def filter_by_tags(log_entries, tags):
    for tag in tags:
        log_entries = filter_by_tag(log_entries, tag)
    return log_entries

def filter_by_region(log_entries, region):
    return filter(lambda e : 'region' in e and e['region'] == region, log_entries)

def filter_by_store(log_entries, store):
    return filter(lambda e : 'store' in e and e['store'] == store, log_entries)

def filter_by_word(log_entries, word):
    return filter(lambda e : word in e['content'], log_entries)

def filter_by_pattern(log_entries, pattern):
    p = re.compile(pattern)
    return filter(lambda e: p.search(e['content']) is not None, log_entries)

# 如何抽取一部分 log, 大概的接口，具体实现再议
# 1. 传入filters，按自定义的filter函数过滤
# 2. 传入字段名称，自己判断
def filter_log_entries(log_entries, **kw):
    res = log_entries

    if 'filters' in kw:
        filters = kw['filters']
        for f in filters:
            res = filter(f, res)

    if 'datetime' in kw:
        res = filter_by_datetime(res, kw['datetime'][0], kw['datetime'][1])

    if 'date' in kw:
        res = filter_by_date(res, kw['date'][0], kw['date'][1])

    if 'level' in kw:
        res = filter_by_level(res, kw['level'])

    if 'filename' in kw:
        res = filter_by_filename(res, kw['filename'])

    if 'tags' in kw:
        res = filter_by_tags(res, kw['tags'])

    if 'region' in kw:
        res = filter_by_region(res, kw['region'])

    if 'store' in kw:
        res = filter_by_store(res, kw['store'])

    if 'word' in kw:
        res = filter_by_word(res, kw['word'])

    if 'pattern' in kw:
        res = filter_by_pattern(res, kw['pattern'])

    return res
