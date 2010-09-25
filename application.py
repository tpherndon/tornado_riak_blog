import tornado

import os

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "F5Rc$aC*W__TrwA8F+4Np-8rZfEonm_YOVtuwRwkO4CtSShr)kV%zBtII__aqZH4",
    "login_url": "/login",
    "xsrf_cookies": True,
    }

application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/article/(w+)", ArticleHandler,
    (r"/login", LoginHandler),
    (r"/about", AboutHandler),
    (r"/projects", ProjectHandler),
    (r"/feed", FeedHandler),
    (r"/admin", EntryListHandler),
    (r"/admin/new", NewEntryHandler),
    (r"/admin/edit/(w+)", EditEntryHandler),
    (r"/admin/delete/(w+)", DeleteEntryHandler),
    ])
