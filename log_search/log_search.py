#!/usr/bin/env python3

from pprint import pprint
from log_entry import entry
from log_entry import parser
from log_entry import formatter
from detection import slow_query
from glob import glob


def print_help():
    help_doc = '''
    Usage:
    --input                     log文件
    --log_type                  log 类型：TIDB/TIKV/PD
    --datetime-begin            开始时间 'YYYY/MM/DD HH:MM:SS'
    --datetime-end              结束时间 'YYYY/MM/DD HH:MM:SS'
    --date-begin                开始日期 'YYYY/MM/DD'
    --date-end                  结束日期 'YYYY/MM/DD'
    --tags                      tag1,tag2,...    e.g. SLOW_QUERY
    --level                     DEBUG/INFO/WARN/ERROR
    --filename                  源码文件名
    --region                    TiKV region
    --store                     TiKV store
    --word                      按关键字搜索
    --pattern                   按正则表达式搜索
    '''
    print(help_doc)


def parse_args(args):
    is_key = lambda x: x.startswith('-') or x.startswith('--')

    kw = {}
    index = 0
    while index < len(args):
        curr = args[index]
        if is_key(curr):
            if '=' in curr:
                k, v = curr.split('=')
                k = k.lstrip('-')
                kw[k] = v
                index += 1
            elif index + 1 == len(args) or is_key(args[index + 1]):
                k = curr.lstrip('-')
                kw[k] = True
                index += 1
            else:
                k = curr.lstrip('-')
                v = args[index + 1]
                kw[k] = v
                index += 2
        else:
            raise Exception('Bad argument, expect key but got: {}'.format(curr))

    return kw

def log_level_str_to_int(level):
    return {
        'd': entry.LOG_DEBUG,
        'i': entry.LOG_INFO,
        'w': entry.LOG_WARN,
        'e': entry.LOG_ERROR,
        'f': entry.LOG_FATAL,
        'n': entry.LOG_NULL,
    }[level.lower()[0]]


def search_cli():
    input_text = open(kw['input']).read()
    raw_entries = parser.parse_text(input_text, kw['log_type'])

    if 'datetime-begin' in kw and 'datetime-end' in kw:
        kw['datetime'] = (kw['datetime-begin'], kw['datetime-end'])

    if 'date-begin' in kw and 'date-end' in kw:
        kw['date'] = (kw['date-begin'], kw['date-end'])

    if 'tags' in kw:
        kw['tags'] = kw['tags'].split(',')

    if 'level' in kw:
        kw['level'] = log_level_str_to_int(kw['level'])

    res = entry.filter_log_entries(raw_entries, **kw)

    format_res = map(formatter.format_log_entry, res)
    for r in format_res:
        print(r)

def slow_query_cli():
    kv_input_files = glob(kw['kv-inputs'])
    db_input_files = glob(kw['db-inputs'])

    # print(kv_input_files, db_input_files)

    kv_logs = [parser.parse_text(open(f).read(), entry.SOURCE_TIKV) for f in kv_input_files]
    db_logs = [parser.parse_text(open(f).read(), entry.SOURCE_TIDB) for f in db_input_files]

    for db_log in db_logs:
        for kv_log in kv_logs:
            res = slow_query.slow_query_detect(db_log, kv_log)
            print(res)


def main(kw):
    if 'help' in kw:
        print_help()
    elif 'input' in kw:
        search_cli()
    elif 'kv-inputs' in kw and 'db-inputs' in kw:
        slow_query_cli()
    else:
        print_help()

if __name__ == '__main__':
    import sys
    kw = parse_args(sys.argv[1:])
    main(kw)
