#!/bin/sh

runtests() {
    cd "$1"
    coverage run --branch --source ../url2feed,. -m unittest discover
    coverage report --omit 'test_*'
    coverage html --omit 'test_*'
}

roottestdir="`pwd`/`dirname $0`"
(runtests "$roottestdir")

