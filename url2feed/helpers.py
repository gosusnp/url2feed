#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

import urlparse

def clean_url(url, base):
    """Normalize urls http://<host><path>?<params>"""
    if not url.startswith('http'):
        url = urlparse.urljoin(base, url)
    return urlparse.urldefrag(url)[0]

def create_candidate(f, url):
    """Extract useful information from feed

    title: title of the feed
    link: link declared in the feed
    url: url of the feed
    sublinks: links of the items of the feed

    """
    candidate = {'url': url, 'sublinks': []}
    try:
        candidate['link'] = f.feed.link
    except AttributeError:
        candidate['link'] = ''
    else:
        candidate['link'] = clean_url(candidate['link'], url)
    try:
        candidate['title'] = f.feed.title
    except AttributeError:
        candidate['title'] = ''
    try:
        for e in f.entries:
            try:
                candidate['sublinks'].append(e.link)
            except AttributeError:
                pass
    except AttributeError:
        pass
    return candidate

def url_match(lhs, rhs):
    """Compare urls"""
    def add_to_set(url, s):
        if url.endswith('/'):
            s.add(url[:-1])
        else:
            s.add(url)
    set1 = set()
    set2 = set()
    for u, s in ((lhs, set1), (rhs, set2)):
        if isinstance(u, (unicode, str)):
            add_to_set(u, s)
        else:
            for i in u:
                add_to_set(i, s)
    return set1 & set2

