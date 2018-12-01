import sys
import signal
import threading
from datetime import datetime, timedelta

import tornado.ioloop
import tornado.web
import tornado.locale
import tornado.httpserver

from settings import site_settings
from api.api import alert_messages, unique_alert_messages
from log_puller.puller import pull
import urls
import util

time_window = datetime.now() - timedelta(seconds=300)


def alert_listener():
    global time_window
    while True:
        msg = alert_messages.get()
        if msg is None:
            break
        if datetime.now() - time_window > timedelta(seconds=300):
            pull()
            time_window = datetime.now()
            unique_alert_messages = set()


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except (TypeError, IndexError):
        port = site_settings['port']
    mapping = util.generate_url(urls.urls, urls.apps, __name__)
    application = tornado.web.Application(mapping, **site_settings)

    server = tornado.httpserver.HTTPServer(application, xheaders=True)
    server.listen(port)
    bg_thread = threading.Thread(target=alert_listener)
    bg_thread.setDaemon(True)
    bg_thread.start()
    tornado.ioloop.IOLoop.current().start()
