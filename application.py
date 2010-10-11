import tornado
import tornado.web
import tornado.httpserver

import os

from handlers import *

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "F5Rc$aC*W__TrwA8F+4Np-8rZfEonm_YOVtuwRwkO4CtSShr)kV%zBtII__aqZH4",
    "login_url": "/login",
    "xsrf_cookies": True,
    "riak_host": "127.0.0.1",
    "riak_port": 8091,
    "riak_prefix": "riak",
    "riak_mapred_prefix": "mapred",
    "index_number": 8,
    }

application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/article/(w+)", ArticleHandler, settings),
    (r"/login", LoginHandler),
    (r"/about", AboutHandler),
    (r"/projects", ProjectHandler),
    (r"/feed", FeedHandler),
    (r"/admin", EntryListHandler),
    (r"/admin/new", NewEntryHandler),
    (r"/admin/edit/(w+)", EditEntryHandler),
    (r"/admin/delete/(w+)", DeleteEntryHandler),
    (r"/admin/test_riak/ping", RiakPingTestHandler, settings),
    (r"/admin/test_riak/get", RiakGetTestHandler, settings),
    (r"/admin/test_riak/put", RiakPutTestHandler, settings),
    (r"/admin/test_riak/keys", RiakKeysTestHandler, settings),
    (r"/admin/test_riak/props", RiakPropsTestHandler, settings),
    (r"/admin/test_riak/delete", RiakDeleteTestHandler, settings),
    ], **settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

