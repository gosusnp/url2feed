url2feed
========

Extract feed url from url.

Usage
-----

From source:

    >>> from url2feed import extract
    >>> print extract('www.metalhammer.co.uk')
    {
        'link': 'http://www.metalhammer.co.uk',
        'url': 'http://feeds.feedburner.com/metalhammer/main',
        'title': 'Metal Hammer',
    }

From command line:

    $ url2feed www.metalhammer.co.uk
    > www.metalhammer.co.uk
       webpage  : http://www.metalhammer.co.uk
       feedurl  : http://feeds.feedburner.com/metalhammer/main
       feedtitle: Metal Hammer

[![githalytics.com alpha](https://cruel-carlota.pagodabox.com/f817085cce31a78a5cf37a2ce7274519 "githalytics.com")](http://githalytics.com/gosusnp/url2feed)
