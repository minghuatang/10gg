from log_entry import entry
from slow_query import slow_query_detect

def detect(tidb_logs, tikv_logs):
    slow_query_detect(tidb_logs,tikv_logs)