# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

import unittest

from url2feed.fetcher import \
        extract_netloc_path,\
        fetch,\
        follow_redirect

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
        # TODO write test using a naive webserver on localhost
        pass

    def test_fetch(self):
        # TODO write test using a naive webserver on localhost
        pass


if __name__ == '__main__':
    unittest.main()

