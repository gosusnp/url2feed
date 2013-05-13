#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

from url2feed import extract

URLS = [
    'http://www.lemonde.fr',
    'lesechos.fr',
    'http://www.lefigaro.fr',
    'www.lepoint.fr',
    'http://www.cnn.com',
    'http://www.bbc.co.uk/news',
    'http://news.cnet.com',
    'korben.info',
    'http://snowboarding.transworld.net/',
    'http://www.metalhammer.co.uk',
    'http://blog.syllabs.com/cartographie-de-la-notion-de-reputation-revue-tank',
]

def main():
    for url in URLS:
        print '>', url
        result = extract(url)
        if result is not None:
            print '\t home :', result['link']
            print '\t feed :', result['url']
            print '\t title:', result['title']

if __name__ == '__main__':
    main()

