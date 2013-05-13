#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

import httplib
import urlparse
import urllib2

def extract_netloc_path(url):
    """Extract netloc and path from url"""
    parsed_url = urlparse.urlparse(url)
    return parsed_url.netloc, parsed_url.path

def follow_redirect(url, max_redirect=5):
    """Follow redirections

    Return a list of followed urls

    """
    netloc, path = extract_netloc_path(url)

    status = 0
    redirect = []
    while True:
        redirect.append('http://%s%s' % (netloc, path))
        if len(redirect) > max_redirect:
            break

        conn = httplib.HTTPConnection(netloc)
        conn.request("HEAD", path)
        response = conn.getresponse()

        status = response.status
        if status in (301, 302):
            try:
                newloc = dict(response.getheaders())['location']
            except KeyError:
                assert False # handle this case
            else:
                tmp_netloc, path = extract_netloc_path(newloc)
                if tmp_netloc:
                    netloc = tmp_netloc
                if not path.startswith('/'):
                    path = '/' + path
                continue
        # FIXME do something when status is not in (200, 301, 302)?
        break
    return redirect if status == 200 else []

def fetch(url):
    """Fetch url

    return <list of urls>, <content>

    """
    if not url.startswith('http'):
        for prefix in ('http://', 'http://www.'):
            urls = follow_redirect(prefix + url)
            if urls:
                break
    else:
        urls = follow_redirect(url)

    if urls:
        data = urllib2.urlopen(urls[-1])
        if data.getcode() == 200:
            content = data.read()
            final_url = data.geturl()
            assert final_url == urls[-1]
            return urls, content
        else:
            assert False # FIXME
    else:
        assert False # FIXME

