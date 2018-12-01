#!/usr/bin/env python3

def format_log_level(level):
    return [
        'DEBUG',
        'INFO ',
        'WARN ',
        'ERROR',
        'FATAL',
    ][level]

def format_log_type(log_type):
    return log_type.lstrip('TI')

def format_log_entry(log_entry):
    return '{} {} {}:{} {}'.format(
        log_entry['log_time'],
        format_log_level(log_entry['log_level']),
        log_entry['file_name'],
        log_entry['file_line'],
        log_entry['content'],
    )

def format_log_entry_with_type(log_entry):
    return '{} {} {} {}:{} {}'.format(
        format_log_type(log_entry['log_type']),
        log_entry['log_time'],
        format_log_level(log_entry['log_level']),
        log_entry['file_name'],
        log_entry['file_line'],
        log_entry['content'],
    )
