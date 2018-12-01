import os
import json
from datetime import (datetime, timedelta)
import queue
import threading

import tornado.web
import tornado.websocket
import tornado.gen
from tornado.queues import Queue

import log_puller
import log_entry.parser as parser
import log_entry.entry as entry
from detection import detect
from settings import site_settings

LOGS = dict()
LAST_SESSION_ID = 0
alert_messages = Queue()
unique_alert_messages = set()
websocket_connections = set()


class AlertHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        global alert_messages, unique_alert_messages
        print(self.request.body)
        data = self.request.body.decode()
        data_json = json.loads(data)
        alert_info = data_json['alerts'][0]
        alert_label = alert_info['labels']
        alert_msg = {}
        alert_msg['alertname'] = alert_label['alertname']
        alert_msg['startsAt'] = alert_info['startsAt']
        alert_name = alert_msg['alertname']
        print(alert_name)
        if alert_name in unique_alert_messages:
            self.finish()
            return
        unique_alert_messages.add(alert_name)
        yield alert_messages.put(alert_msg)
        self.finish()


def load_logs(data_dir):
    logs = dict(tidb=[], tikv=[], pd=[])
    for filename in os.listdir(data_dir):
        path = os.path.join(data_dir, filename)
        if os.path.isdir(path):
            l = load_logs(path)
            return merge_logs(logs, l)
        f = open(path, 'r')
        if "tidb" in filename:
            logs["tidb"].append(dict(
                name=filename.split('-')[0],
                logs=parser.parse_text(f.read(), entry.SOURCE_TIDB)
            ))
        elif "tikv" in filename:
            logs["tikv"].append(dict(
                name=filename.split('-')[0],
                logs=parser.parse_text(f.read(), entry.SOURCE_TIKV)
            ))
        elif "pd" in filename:
            logs["pd"].append(dict(
                name=filename.split('-')[0],
                logs=parser.parse_text(f.read(), entry.SOURCE_PD)
            ))
    return logs


def merge_logs(logs, l):
    for k in logs.keys():
        logs[k] += l[k]
    return logs


class LogPullHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def on_message(self, message):
        global LOGS, LAST_SESSION_ID
        args = json.loads(message)
        ring_time = datetime.strptime(args['ring_time'][:19], '%Y-%m-%d %H:%M:%S')
        LAST_SESSION_ID += 1
        session_id = LAST_SESSION_ID
        data_dir = site_settings['data_path']
        log_puller.pull()
        logs = load_logs(data_dir)
        LOGS[session_id] = logs
        delta = timedelta(hours=1)
        time_start = datetime.strftime(ring_time-delta, "%Y/%m/%d %H:%M:%S")
        time_end = datetime.strftime(ring_time+delta, "%Y/%m/%d %H:%M:%S")
        length = 0
        for cluster, cluster_logs in logs.items():
            for l in cluster_logs:
                l['logs'] = list(entry.filter_log_entries(l['logs'],
                                                          level=entry.LOG_ERROR,
                                                          datetime=[time_start, time_end]))
                length += len(l['logs'])
        logs['time_start'] = time_start
        logs['time_end'] = time_end
        print(length)

        self.write_message(json.dumps(
            dict(logs=logs,
                 session_id=session_id
                 ))
        )
        self.close()


class MetricsRingHandler(tornado.websocket.WebSocketHandler):
    closed = False

    def check_origin(self, origin):
        return True

    @tornado.gen.coroutine
    def on_message(self, msg):
        global alert_messages
        while True:
            msg = yield alert_messages.get()
            if msg is None and not self.closed:
                break
            t = datetime.strptime(msg['startsAt'][:-16], '%Y-%m-%dT%H:%M:%S')
            self.write_message(json.dumps([{
                "text": msg['alertname'],
                "link": "/log?ring_time={}".format(t.strftime("%Y/%m/%d %H:%M:%S"))
            }]))

    def on_close(self):
        self.closed = True


class LogTipsHandler(tornado.web.RequestHandler):
    def get(self):
        global LOGS
        session_id = int(self.get_query_argument('session_id'))
        logs = LOGS[session_id]
        result = detect.analyze(datetime=[logs['time_start'], logs['time_end']])
        unique = set()
        ret = []
        for r in result:
            if r["rewrite"] in unique:
                continue
            unique.add(r["rewrite"])
            ret.append(r)
        self.finish(json.dumps(ret))


class LogFilterHandler(tornado.web.RequestHandler):
    def post(self):
        global LOGS
        session_id = int(self.get_query_argument('session_id'))
        args = self.request.body.decode('utf8')
        logs = LOGS[session_id]
        for cluster, cluster_logs in logs.items():
            for l in cluster_logs:
                l['logs'] = list(entry.filter_log_entries(l['logs'],
                                                          **json.loads(args)))
        self.finish(json.dumps(logs))
