import base64
import random
import urllib
import urlparse

from tornado import httpclient


class RiakTornadoClient(object):
    def __init__(self, host='127.0.0.1', port=8098, prefix='riak', mapred_prefix='mapred', client_id=None):
        """Construct a new Tornado client for Riak. Copied from RiakHttpClient in large part."""
        self._host = host
        self._port = port
        self._prefix = prefix
        self._mapred_prefix = mapred_prefix
        self._client_id = client_id
        if not self._client_id:
            self._client_id = 'py_%s' % base64.b64encode(
                str(random.randint(1, 1073741824)))
        self._client = httpclient.AsyncHTTPClient()

    def build_rest_url(self, bucket=None, key=None, path=None, query='', fragment=''):
        if not bucket and not path:
            raise Exception("You need to supply either a bucket value or a path value.")
        if bucket:
            url = ''.join(('/', self._prefix))
            url = '/'.join((url, urllib.quote_plus(bucket.get_name())))

        if key:
            url = '/'.join((url, urllib.quote_plus(key)))

        if path:
            # If the user specifies a path, use that path and nothing else
            # Thus, ditch the bucket, key, prefix, etc.
            url = path

        if query:
            q_items = ['='.join((urllib.quote_plus(k), urllib.quote_plus(str(v)))) for k,v in query.items()]
            query = '&'.join(q_items)

        loc = ':'.join((self._host, str(self._port)))
        scheme = 'http'
        netloc = loc
        path = url

        url_parts = (scheme, netloc, path, query, fragment)
        return urlparse.urlunsplit(url_parts)

    def to_link_header(self, link):
        header = '/'.join(('<', self._prefix, urllib.quote_plus(link.get_bucket()),
                           urllib.quote_plus(link.get_key())))
        header = ''.join((header, '>; riaktag="', urllib.quote_plus(link.get_tag()), '"'))

        return header

    def ping(self, callback):
        url = self.build_rest_url(path='/ping')
        self._client.fetch(url, callback)

    def get(self, callback, robj, r=1, vtag=None):
        query = {'r': r}
        if vtag:
            query['vtag'] = vtag

        url = self.build_rest_url(robj.get_bucket(), robj.get_key(), query=query)
        self._client.fetch(url, callback)

    def put(self, callback, robj, w=1, dw=1, return_body=True):
        query = {'w': w, 'dw': dw}
        if return_body:
            query['returnbody'] = 'true'

        url = self.build_rest_url(robj.get_bucket(), robj.get_key(), query=query)

        headers = {'Accept': 'text/plain, */*; q=0.5',
                   'Content-Type': robj.get_content_type(),
                   'X-Riak-ClientId': self._client_id}

        if robj.vclock():
            headers['X-Riak-Vclock'] = robj.vclock()

        if robj.get_links():
            link_body = ', '.join([self.to_link_header(link) for link in robj.get_links()])
            headers['Link'] = link_body

        request = httpclient.HTTPRequest(url, 'PUT', headers, robj.get_data())
        self._client.fetch(request, callback)

    def delete(self, callback, robj, rw=1):
        query = {'rw': rw}

        url = self.build_rest_url(robj.get_bucket(), robj.get_key(), query=query)
        request = httpclient.HTTPRequest(url, 'DELETE')
        self._client.fetch(request, callback)

    def get_keys(self, callback, bucket):
        query = {'props': 'true', 'keys': 'true'}
        url = self.build_rest_url(bucket, query=query)
        print "keys url: ", url
        self._client.fetch(url, callback)

    def get_bucket_props(self, callback, bucket):
        query = {'props': 'true', 'keys': 'false'}
        url = self.build_rest_url(bucket, query=query)
        print "props url: ", url
        self._client.fetch(url, callback)

    def set_bucket_props(self, callback, bucket, props):
        url = self.build_rest_url(bucket)
        headers = {'Content-Type': 'application/json'}
        content = json.dumps({'props': props})
        request = httpclient.HTTPRequest(url, 'PUT', headers=headers, body=content)
        self._client.fetch(request, callback)

    def mapred(self, callback, inputs, query, timeout=None):
        job = {'inputs': inputs, 'query': query}
        if timeout:
            job['timeout'] = timeout

        content = json.dumps(job)
        url = self.build_rest_url(path=''.join(('/', self._mapred_prefix)))
        request = httpclient.HTTPRequest(url, 'PUT', body=content)
        self._client.fetch(request, callback)



