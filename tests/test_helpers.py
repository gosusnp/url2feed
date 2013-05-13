# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

import unittest

from url2feed.helpers import clean_url, create_candidate, url_match

class InnerFeed(object):
    def __init__(self, link, title):
        if link is not None:
            self.link = link
        if title is not None:
            self.title = title
class Feed(object):
    def __init__(self, link, title, entries):
        if link is not None or title is not None:
            self.feed = InnerFeed(link, title)
        if entries is not None:
            self.entries = entries

class TestHelpers(unittest.TestCase):
    def test_clean_url(self):
        self.assertEqual(
                clean_url('http://www.myhost.com', 'http://www.myhost.com'),
                'http://www.myhost.com')
        self.assertEqual(
                clean_url('index', 'http://www.myhost.com'),
                'http://www.myhost.com/index')
        self.assertEqual(
                clean_url('/index', 'http://www.myhost.com'),
                'http://www.myhost.com/index')
        self.assertEqual(
                clean_url('/index#hashtag', 'http://www.myhost.com'),
                'http://www.myhost.com/index')
        self.assertEqual(
                clean_url('/index?params#hashtag', 'http://www.myhost.com'),
                'http://www.myhost.com/index?params')

    def test_url_match(self):
        self.assertTrue(url_match('http://www.myhost.com', 'http://www.myhost.com'))
        self.assertTrue(url_match('http://www.myhost.com', 'http://www.myhost.com/'))
        self.assertTrue(url_match('http://www.myhost.com/', 'http://www.myhost.com'))
        self.assertTrue(url_match('http://www.myhost.com/', 'http://www.myhost.com/'))
        self.assertFalse(url_match('http://www.myhost.com', 'http://www.myhost.com?params'))
        self.assertFalse(url_match('http://www.myhost.com', 'http://www.myhost.com#hash'))

         # TODO Write tests using sets of urls

    def test_create_candidate(self):
        self.assertEqual(
                create_candidate(
                    Feed('http://www.myhost.com/', 'MyHost', None),
                    'http://www.myhost.com/rss'),
                {
                    'url': 'http://www.myhost.com/rss',
                    'link': 'http://www.myhost.com/',
                    'title': 'MyHost',
                    'sublinks': [],
                })
        self.assertEqual(
                create_candidate(
                    Feed('http://www.myhost.com/', None, None),
                    'http://www.myhost.com/rss'),
                {
                    'url': 'http://www.myhost.com/rss',
                    'link': 'http://www.myhost.com/',
                    'title': '',
                    'sublinks': [],
                })
        self.assertEqual(
                create_candidate(
                    Feed(None, 'MyHost', None),
                    'http://www.myhost.com/rss'),
                {
                    'url': 'http://www.myhost.com/rss',
                    'link': '',
                    'title': 'MyHost',
                    'sublinks': [],
                })
        self.assertEqual(
                create_candidate(
                    Feed(None, None, None),
                    'http://www.myhost.com/rss'),
                {
                    'url': 'http://www.myhost.com/rss',
                    'link': '',
                    'title': '',
                    'sublinks': [],
                })
        self.assertEqual(
                create_candidate(
                    Feed('http://www.myhost.com/', 'MyHost', [InnerFeed('http://www.myhost.com/subs', 'MyHost subs')]),
                    'http://www.myhost.com/rss'),
                {
                    'url': 'http://www.myhost.com/rss',
                    'link': 'http://www.myhost.com/',
                    'title': 'MyHost',
                    'sublinks': ['http://www.myhost.com/subs'],
                })
        self.assertEqual(
                create_candidate(
                    Feed('http://www.myhost.com/', 'MyHost', [InnerFeed('http://www.myhost.com/subs', 'MyHost subs'), InnerFeed(None, 'ho!')]),
                    'http://www.myhost.com/rss'),
                {
                    'url': 'http://www.myhost.com/rss',
                    'link': 'http://www.myhost.com/',
                    'title': 'MyHost',
                    'sublinks': ['http://www.myhost.com/subs'],
                })

if __name__ == '__main__':
    unittest.main()

