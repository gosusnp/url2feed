# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

import unittest

from url2feed.url2feed import \
        extract_feeds,\
        expand_feeds,\
        filter_expanded_feeds,\
        extract

WEBPAGE = """<html>
<head>
<link rel="alternative" type="application/rss+xml" title="feed1" href="http://myhost.fr/rss" />
<link rel="alternative" type="application/rss+xml" title="feed2" href="/rss" />
<link rel="alternative" type="application/rss+xml" title="nolink" />
</head>
<body>
</body>
</html>"""

class TestURL2FEED(unittest.TestCase):
    def test_extract_feeds(self):
        self.assertEqual(extract_feeds(WEBPAGE, "http://www.myhost.fr"),
                [u'http://myhost.fr/rss', u'http://www.myhost.fr/rss'])

    def test_expand_feeds(self):
        pass # FIXME

    def test_filter_expanded_feeds(self):
        self.assertEqual(
                filter_expanded_feeds(
                    [u'http://www.myhost.fr'],
                    [{'title': 'Feed1', u'link': 'http://myhost.fr/', u'url': u'http://myhost.fr/rss'},
                     {'title': 'Feed1', u'link': 'http://www.myhost.fr/', u'url': u'http://www.myhost.fr/rss'}]),
                [{'title': 'Feed1', u'link': 'http://www.myhost.fr/', u'url': u'http://www.myhost.fr/rss'}])

    def test_extract(self):
        pass # FIXME


if __name__ == '__main__':
    unittest.main()

