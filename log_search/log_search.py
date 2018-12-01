#!/usr/bin/env python3

from pprint import pprint
from log_entry import entry
from log_entry import parser

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


def main(kw):
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

    pprint(list(res))


if __name__ == '__main__':
    import sys
    kw = parse_args(sys.argv[1:])
    main(kw)
