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
    def test_extract_netloc_path__no_path(self):
        self.assertEqual(
                extract_netloc_path('http://www.myhost.com'),
                ('www.myhost.com', ''))

    def test_extract_netloc_path__path_is_slash(self):
        self.assertEqual(
                extract_netloc_path('http://www.myhost.com/'),
                ('www.myhost.com', '/'))

    def test_extract_netloc_path__with_path_and_params(self):
        self.assertEqual(
                extract_netloc_path('http://www.myhost.com/test?params=true'),
                ('www.myhost.com', '/test'))

    def test_extract_netloc_path__with_path_and_hash(self):
        self.assertEqual(
                extract_netloc_path('http://www.myhost.com/#hash'),
                ('www.myhost.com', '/'))

    def test_extract_netloc_path__with_path_params_and_hash(self):
        self.assertEqual(
                extract_netloc_path('http://www.myhost.com/ultimate?params=true#hash'),
                ('www.myhost.com', '/ultimate'))

    def test_follow_redirect__basic(self):
        self.assertEqual(
                follow_redirect('http://myhost.com'),
                ['http://myhost.com', 'http://www.myhost.com/'])

    def test_follow_redirect__complete_relative_location(self):
        self.assertEqual(
                follow_redirect('http://www.myhost.com/noslash'),
                ['http://www.myhost.com/noslash', 'http://www.myhost.com/slashless'])

    def test_follow_redirect__no_crash_on_missing_location(self):
        self.assertEqual(
                follow_redirect('http://www.myhost.com/nolocation'),
                [])

    def test_follow_redirect__test_max_redirect(self):
        self.assertEqual(
                follow_redirect('http://www.myhost.com/loop'),
                [])

    def test_follow_redirect__badhost(self):
        self.assertEqual(
                follow_redirect('http://badhost'),
                [])

    def test_fetch__std_url(self):
        self.assertEqual(fetch('http://myhost.com'),
                (['http://myhost.com', 'http://www.myhost.com/'], 'content!'))

    def test_fetch__domain_name_only(self):
        self.assertEqual(fetch('myhost.com'),
                (['http://myhost.com', 'http://www.myhost.com/'], 'content!'))

    def test_fetch__do_not_crash_1(self):
        self.assertEqual(fetch('myhost.com/unexpected_failure500'), None)

    def test_fetch__do_not_crash_2(self):
        self.assertEqual(fetch('myhost.com/unexpected_failure204'), None)

    def test_fetch__do_not_crash_3(self):
        self.assertEqual(fetch('badhost'), None)


if __name__ == '__main__':
    unittest.main()

