# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

import httplib
import unittest
import StringIO

from url2feed.fetcher import \
        extract_netloc_path,\
        fetch,\
        follow_redirect

class MockResponse(object):
    def __init__(self, status, headers, content=None):
        self.status = status
        self.__headers = headers
        if content is not None:
            self.msg = StringIO.StringIO(content)
        self.reason = 'OK'
    def getheaders(self):
        return self.__headers
    def read(self, *args, **kwargs):
        return self.msg.read()

class MockHTTPConnection(object):
    def __init__(self, netloc, *args, **kwargs):
        if netloc not in ('myhost.com', 'www.myhost.com'):
            raise httplib.HTTPException(netloc)
        self.netloc = netloc
        self.path = None
        self.method = None
        self.response = {}
    def set_debuglevel(*args, **kwargs):
        pass
    def request(self, method, path, *args, **kwargs):
        self.path = path
        self.method = method
    def getresponse(self):
        if self.method == 'HEAD':
            if self.netloc == 'myhost.com':
                if self.path.startswith('/unexpected_failure'):
                    return MockResponse(500, {})
                else:
                    return MockResponse(301, {'location': 'http://www.myhost.com/'})
            elif self.netloc == 'www.myhost.com':
                if self.path == '/':
                    return MockResponse(200, {})
                elif self.path == '/noslash':
                    return MockResponse(302, {'location': 'slashless'})
                elif self.path == '/slashless':
                    return MockResponse(200, {})
                elif self.path == '/nolocation':
                    return MockResponse(301, {})
                elif self.path.startswith('/unexpected_failure'):
                    return MockResponse(200, {})
                elif self.path == '/unexpected_failure':
                    return MockResponse(200, {})
                elif self.path.startswith('/loop'):
                    return MockResponse(301, {'location': self.path + '-'})
                else:
                    assert False
            else:
                assert False
        elif self.method == 'GET':
            if self.path == '/':
                return MockResponse(200, {}, 'content!')
            elif self.path == '/unexpected_failure204':
                return MockResponse(204, {}, 'Fail')
            elif self.path == '/unexpected_failure500':
                return MockResponse(500, {}, 'Fail')
        else:
            assert False
httplib.HTTPConnection = MockHTTPConnection

class TestFetcher(unittest.TestCase):
    def test_extract_netloc_path(self):
        self.assertEqual(
                extract_netloc_path('http://www.myhost.com'),
                ('www.myhost.com', ''))
        self.assertEqual(
                extract_netloc_path('http://www.myhost.com/'),
                ('www.myhost.com', '/'))
        self.assertEqual(
                extract_netloc_path('http://www.myhost.com/test?params=true'),
                ('www.myhost.com', '/test'))
        self.assertEqual(
                extract_netloc_path('http://www.myhost.com/#hash'),
                ('www.myhost.com', '/'))
        self.assertEqual(
                extract_netloc_path('http://www.myhost.com/ultimate?params=true#hash'),
                ('www.myhost.com', '/ultimate'))

    def test_follow_redirect(self):
        self.assertEqual(
                follow_redirect('http://myhost.com'),
                ['http://myhost.com', 'http://www.myhost.com/'])
        self.assertEqual(
                follow_redirect('http://www.myhost.com/noslash'),
                ['http://www.myhost.com/noslash', 'http://www.myhost.com/slashless'])
        self.assertEqual(
                follow_redirect('http://www.myhost.com/nolocation'),
                [])
        self.assertEqual(
                follow_redirect('http://www.myhost.com/loop'),
                [])
        self.assertEqual(
                follow_redirect('http://badhost'),
                [])

    def test_fetch(self):
        self.assertEqual(fetch('http://myhost.com'),
                (['http://myhost.com', 'http://www.myhost.com/'], 'content!'))
        self.assertEqual(fetch('myhost.com'),
                (['http://myhost.com', 'http://www.myhost.com/'], 'content!'))
        self.assertEqual(fetch('myhost.com/unexpected_failure500'), None)
        self.assertEqual(fetch('myhost.com/unexpected_failure204'), None)
        self.assertEqual(fetch('badhost'), None)


if __name__ == '__main__':
    unittest.main()

