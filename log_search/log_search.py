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


def main(kw):
    pprint(kw)


if __name__ == '__main__':
    import sys
    kw = parse_args(sys.argv[1:])
    main(kw)
