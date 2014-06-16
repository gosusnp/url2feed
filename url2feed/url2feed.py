#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

from bs4 import BeautifulSoup
import feedparser

from fetcher import fetch, follow_redirect
from helpers import clean_url, create_candidate, url_match

def is_feed_link(tag):
    return tag['type'] == 'application/rss+xml' or tag['type'] == 'application/atom+xml' if tag.name == 'link' and tag.has_attr('type') else False

def extract_feeds(html, url):
    """Extract feed urls from webpage"""
    w = BeautifulSoup(html) # FIXME handle errors
    feeds = []
    for node in w.find_all(is_feed_link):
        try:
            feed_url = node['href']
        except KeyError:
            pass
        else:
            feeds.append(clean_url(feed_url, url))
    return feeds


def expand_feeds(feeds):
    """Get feed information from feed url"""
    result = []
    for feedurl in feeds:
        f = feedparser.parse(feedurl)
        details = create_candidate(f, feedurl)
        if details['link']:
            details['link'] = follow_redirect(details['link'])
        result.append(details)
    return result


def filter_expanded_feeds(urls, expanded_feeds):
    """Filter expanded feeds"""
    results = []
    for f in expanded_feeds:
        if url_match(urls, f['link']):
            results.append(f)
    return results


def extract(entrypoint):
    """Extract feed from entrypoint

    Entrypoint can be a full url or a domain name. When a domain name
    is given, it attempts to guess the homepage where it can extract
    the feed.

    """
    fetched_data = fetch(entrypoint)
    if fetched_data is None:
        return None
    else:
        urls, html = fetched_data
    feeds = extract_feeds(html, urls[-1])
    expanded_feeds = expand_feeds(feeds)
    results = filter_expanded_feeds(urls, expanded_feeds)

    # TODO loop toward domain for cases such as http://www.lesechos.fr/economie-politique/france/
    # TODO Scoring based on sublinks? -> http://www.lefigaro.fr

    if results:
        # Temporary behavior
        # on multiple results: select the first one
        # TODO Implement better scoring
        del results[0]['sublinks']
        results[0]['link'] = results[0]['link'][0]
        return results[0]

    return None


def main():
    import os
    import sys

    if len(sys.argv) < 2:
        sys.stderr.write(' usage: %s <urls...>\n' % os.path.basename(sys.argv[0]))
        exit(1)

    stream = sys.stdout
    for url in sys.argv[1:]:
        stream.write((u'> %s\n' % url).encode('utf8'))
        result = extract(url)
        if result is not None:
            stream.write((u'   webpage  : %s\n' % result['link']).encode('utf8'))
            stream.write((u'   feedurl  : %s\n' % result['url']).encode('utf8'))
            stream.write((u'   feedtitle: %s\n' % result['title']).encode('utf8'))
        else:
            stream.write((u'   not found\n').encode('utf8'))
        stream.write('\n')

if __name__ == '__main__':
    main()
