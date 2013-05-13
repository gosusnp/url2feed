from setuptools import setup
import os

version = '0.0.1'

install_requires = [
    'beautifulsoup4',
    'feedparser',
]

entry_points="""
[console_scripts]
url2feed = url2feed.url2feed:main
"""

setup(
        name='url2feed',
        version=version,
        description="Extract feed from url.",
        classifiers=[
            "Environment :: Console",
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python",
            "Topic :: Internet",
        ],
        keywords=['url2feed', 'url', 'rss', 'atom', 'feed'],
        author='snp',
        author_email='gosu.snp@gmail.com',
        url='https://github.com/gosusnp/url2feed',
        license='MIT/X',
        packages=['url2feed'],
        install_requires=install_requires,
        entry_points=entry_points,
)
