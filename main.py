if __name__ == "__main__":
    import sys

    import tornado.ioloop
    import tornado.web
    import tornado.locale
    import tornado.httpserver

    from settings import site_settings
    import urls
    import util

    try:
        port = int(sys.argv[1])
    except (TypeError, IndexError):
        port = site_settings['port']
    mapping = util.generate_url(urls.urls, urls.apps, __name__)
    application = tornado.web.Application(mapping, **site_settings)

    server = tornado.httpserver.HTTPServer(application, xheaders=True)
    server.listen(port)

    tornado.ioloop.IOLoop.current().start()

