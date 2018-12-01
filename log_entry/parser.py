#!/usr/bin/env python3

import re
from pprint import pprint
from log_entry import entry

RE_LOG_SPLIT_PD = re.compile(r'^(\d{4}\/\d\d\/\d\d \d\d:\d\d:\d\d\.\d{3}) (\w+\.\w+):(\d+): \[(\w+)\]', re.M)
RE_LOG_SPLIT_TIDB = RE_LOG_SPLIT_PD
RE_LOG_SPLIT_TIKV = re.compile(r'^(\d{4}\/\d\d\/\d\d \d\d:\d\d:\d\d\.\d{3}) \w+ (\w+\.\w+|\<unknown\>):(\d+): ', re.M)

RE_LOG_SPLIT_MAP = {
    entry.SOURCE_PD: RE_LOG_SPLIT_PD,
    entry.SOURCE_TIDB: RE_LOG_SPLIT_TIDB,
    entry.SOURCE_TIKV: RE_LOG_SPLIT_TIKV,
}


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
            'log_level': text_splits[index+3],
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
            'log_level': text_splits[index+1],
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

    return log_entries

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    log_source = sys.argv[2]
    text = open(filename).read()
    log_entries = parse_text(text, log_source)
    pprint(log_entries)
