#!/usr/bin/env python3

import re
from pprint import pprint
from log_entry import log_entry

RE_LOG_SPLIT = re.compile(r'^(\d{4}\/\d\d\/\d\d \d\d:\d\d:\d\d\.\d{3}) (\w+\.\w+):(\d+): \[(\w+)\]', re.M)

def parse_text(text, log_type):
    log_entries = []

    text_splits = RE_LOG_SPLIT.split(text)
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

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    text = open(filename).read()
    log_entries = parse_text(text, log_entry.SOURCE_PD)
    pprint(log_entries)
