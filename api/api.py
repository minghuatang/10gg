import os
import json

import tornado.web
import tornado.websocket

import log_pull
import log_entry.parser as parser
import log_entry.entry as entry
from settings import site_settings

LOGS = dict()
LAST_SESSION_ID = 0


class AlertHandler(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        pass


class LogPullHandler(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        LAST_SESSION_ID += 1
        session_id = LAST_SESSION_ID
        data_dir = site_settings['data_dir']
        log_pull.pull(site_settings['cluster_config'],
                      site_settings['remote_username'],
                      data_dir)
        logs = load_logs(data_dir)
        LOGS[session_id] = logs
        self.write_message(json.dumps(dict(logs=logs, session_id=session_id)))
        self.close()

        @staticmethod
        def load_logs(data_dir):
            logs = dict(tidb=[], tikv=[], pd=[])
            for filename in os.listdir(data_dir):
                path = os.path.join(data_dir, filename)
                if os.path.isdir(path):
                    l = load_logs(path)
                    logs = merge_logs(logs, l)
                    return
                f = open(path, 'r')
                if "tidb" in filename:
                    logs["tidb"] += parser.parse_text(f.read(), entry.SOURCE_TIDB)
                elif "tikv" in filename:
                    logs["tikv"] += parser.parse_text(f.read(), entry.SOURCE_TIKV)
                elif "pd" in filename:
                    logs["pd"] += parser.parse_text(f.read(), entry.SOURCE_PD)

        @staticmethod
        def merge_logs(logs, l):
            logs["tidb"] += l["tidb"]
            logs["tikv"] += l["tikv"]
            logs["pd"] += l["pd"]
            return logs


class LogTipsHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class LogFilterHandler(tornado.web.RequestHandler):
    def get(self):
        pass
