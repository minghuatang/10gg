from log_entry import entry,parser
from detection.slow_query import slow_query_detect
from os.path import isfile,join
import os 

from settings import site_settings

def analyze():
    files = [f for f in os.listdir(site_settings['data_dir']) if isfile(join(site_settings['data_dir'],f))]
    tikv_entries = []
    tidb_entries = []
    for f in files:
        text = open(os.path.join(site_settings['data_dir'],f)).read()
        if "tikv" in f:
            tikv_entries.extend(list(parser.parse_text(text,entry.SOURCE_TIKV)))
        if "tidb" in f:
            tidb_entries.extend(list(parser.parse_text(text,entry.SOURCE_TIDB)))
    return detect(tidb_entries,tikv_entries) 


def detect(tidb_logs, tikv_logs):
    return slow_query_detect(tidb_logs,tikv_logs)

if __name__ == "__main__":
    print(analyze())    