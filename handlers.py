import tornado
import tornado.web

from riak.riak_object import RiakObject
from riak.bucket import RiakBucket

from riak_client import RiakTornadoClient

class RiakHandler(tornado.web.RequestHandler):
    def initialize(self, **settings):
        self.client = RiakTornadoClient(host=settings['riak_host'],
                port=settings['riak_port'],
                prefix=settings['riak_prefix'],
                mapred_prefix=settings['riak_mapred_prefix'])

    def on_response(self, response):
        if response.error:
            print "response.error:  ", response.error
            print "response: ", response
            print "dir(response): ", dir(response)
            raise tornado.web.HTTPError(500)
        self.write("Response:  " + response.body)
        self.finish()


class IndexHandler(RiakHandler):
    """Returns a list of the settings['index_number'] articles."""
    def get(self):
        # retrieve articles
        pass

class ArticleHandler(RiakHandler):
    def get(self):
        pass

class LoginHandler(RiakHandler):
    def get(self):
        pass

    def post(self):
        pass

class AboutHandler(RiakHandler):
    def get(self):
        pass

class ProjectHandler(RiakHandler):
    def get(self):
        pass

class FeedHandler(RiakHandler):
    def get(self):
        pass

class EntryListHandler(RiakHandler):
    def get(self):
        pass

class NewEntryHandler(RiakHandler):
    def get(self):
        pass

    def post(self):
        pass

class EditEntryHandler(RiakHandler):
    def get(self):
        pass

    def post(self):
        pass

class DeleteEntryHandler(RiakHandler):
    def get(self):
        pass

    def post(self):
        pass

class RiakPingTestHandler(RiakHandler):
    @tornado.web.asynchronous
    def get(self):
        self.client.ping(self.on_response)

    def on_response(self, response):
        if response.error:
            raise tornado.web.HTTPError(500)
        self.write("Ping response: " + response.body)
        self.finish()

class RiakGetTestHandler(RiakHandler):
    @tornado.web.asynchronous
    def get(self):
        bucket = RiakBucket(client=None, name="tornadotest")
        test_object = RiakObject(client=None, bucket=bucket, key="test_object1")

        self.client.get(self.on_response, test_object)

class RiakPutTestHandler(RiakHandler):
    @tornado.web.asynchronous
    def get(self):
        bucket = RiakBucket(client=None, name="tornadotest")
        test_object = RiakObject(client=None, bucket=bucket, key="test_object1")
        test_object.set_content_type("text/plain")
        test_object.set_data("This is a test object")

        self.client.put(self.on_response, test_object)

class RiakKeysTestHandler(RiakHandler):
    @tornado.web.asynchronous
    def get(self):
        bucket = RiakBucket(client=None, name="tornadotest")

        self.client.get_keys(self.on_response, bucket)

class RiakPropsTestHandler(RiakHandler):
    @tornado.web.asynchronous
    def get(self):
        bucket = RiakBucket(client=None, name="tornadotest")

        self.client.get_bucket_props(self.on_response, bucket)

class RiakDeleteTestHandler(RiakHandler):
    @tornado.web.asynchronous
    def get(self):
        bucket = RiakBucket(client=None, name="tornadotest")
        test_object = RiakObject(client=None, bucket=bucket, key="test_object1")

        self.client.delete(self.on_response, test_object)
