#!/usr/bin/env python3

import re
from pprint import pprint
from log_entry import entry

RE_LOG_SPLIT_PD = re.compile(r'^(\d{4}\/\d\d\/\d\d \d\d:\d\d:\d\d\.\d{3}) (\w+\.\w+):(\d+): \[(\w+)\]', re.M)
RE_LOG_SPLIT_TIDB = RE_LOG_SPLIT_PD
RE_LOG_SPLIT_TIKV = re.compile(r'^(\d{4}\/\d\d\/\d\d \d\d:\d\d:\d\d\.\d{3}) (\w+) (\w+\.\w+|\<unknown\>):(\d+): ', re.M)

RE_LOG_SPLIT_MAP = {
    entry.SOURCE_PD: RE_LOG_SPLIT_PD,
    entry.SOURCE_TIDB: RE_LOG_SPLIT_TIDB,
    entry.SOURCE_TIKV: RE_LOG_SPLIT_TIKV,
}

RE_LOG_TAG = re.compile(r'^(\[[^]]+\] )(\[[^]]+\] )*')
RE_LOG_TAG_KV = re.compile(r'(\w+) (\d+)')

# RE_LOG_TAG = re.compile(r'\[([a-zA-Z]\w*)( \d+)?\]')
#
# def parse_tags(log_entry):
#     content = log_entry['content']
#     raw_tags = RE_LOG_TAG.findall(content)
#
#     tags = []
#     for raw_tag in raw_tags:
#         if len(raw_tag) > 1:
#             tag = raw_tag[0]
#             v = raw_tag[1].strip()
#             log_entry[tag] = v
#             tags.append(tag)
#         else:
#             tags.append(raw_tag)
#
#     log_entry['tags'] = tags
#     return log_entry

def parse_tags(log_entry):
    content = log_entry['content']
    res = RE_LOG_TAG.findall(content)

    def prune_raw_tag(raw_tag):
        return raw_tag[1:-2]

    tags = []
    def parse_tag(raw_tag):
        pruned_tag = prune_raw_tag(raw_tag)

        kv_res = RE_LOG_TAG_KV.findall(pruned_tag)
        if 0 != len(kv_res):
            tags.append(kv_res[0][0])
            log_entry[kv_res[0][0]] = kv_res[0][1]
        else:
            tags.append(pruned_tag)

    if 0 != len(res):
        raw_tags = res[0]
        for raw_tag in raw_tags:
            if '' != raw_tag:
                parse_tag(raw_tag)

    log_entry['tags'] = tags
    return log_entry


def parse_log_level_pd_or_tidb(level):
    return {
        'debug':   entry.LOG_DEBUG,
        'info':    entry.LOG_INFO,
        'warning': entry.LOG_WARN,
        'error':   entry.LOG_ERROR,
        'fatal':   entry.LOG_FATAL,
    }[level]

def parse_log_level_tikv(level):
    return {
        'DEBU': entry.LOG_DEBUG,
        'INFO': entry.LOG_INFO,
        'WARN': entry.LOG_WARN,
        'ERRO': entry.LOG_ERROR,
        'FATA': entry.LOG_FATAL,
    }[level]

def parse_text_pd_or_tidb(text, log_type):
    RE_LOG_SPLIT = RE_LOG_SPLIT_MAP[log_type]
    text_splits = RE_LOG_SPLIT.split(text)

    log_entries = []
    index = 1
    while index + 5 < len(text_splits):
        log_entries.append({
            'source':    log_type,
            'log_time':  text_splits[index],
            'file_name': text_splits[index+1],
            'file_line': text_splits[index+2],
            'log_level': parse_log_level_pd_or_tidb(text_splits[index+3]),
            'content':   text_splits[index+4].strip(),
        })
        index += 5

    return log_entries

def parse_text_tikv(text, log_type=entry.SOURCE_TIKV):
    RE_LOG_SPLIT = RE_LOG_SPLIT_MAP[log_type]
    text_splits = RE_LOG_SPLIT.split(text)

    log_entries = []
    index = 1
    while index + 5 < len(text_splits):
        log_entries.append({
            'source':    log_type,
            'log_time':  text_splits[index],
            'log_level': parse_log_level_tikv(text_splits[index+1]),
            'file_name': text_splits[index+2],
            'file_line': text_splits[index+3],
            'content':   text_splits[index+4].strip(),
        })
        index += 5

    return log_entries

def parse_text(text, log_type):
    log_entries = {
        entry.SOURCE_PD: parse_text_pd_or_tidb,
        entry.SOURCE_TIDB: parse_text_pd_or_tidb,
        entry.SOURCE_TIKV: parse_text_tikv,
    }[log_type](text, log_type)

    log_entries = map(parse_tags, log_entries)

    return log_entries

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    log_source = sys.argv[2]
    text = open(filename).read()
    log_entries = parse_text(text, log_source)
    pprint(list(log_entries))
