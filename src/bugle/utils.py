# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'maxwu'

import json
from os import environ
from operator import itemgetter

def beauty_dump(obj):
    return json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': '))


def dict_sort_by_key(d):
    return sorted(d.iteritems(), key=itemgetter(1), reverse=True)


def proxy_decorate(func):
   def func_wrapper(*args, **kwargs):
       _HTTP_PROXY = 'http_proxy'
       proxy = environ[_HTTP_PROXY] if _HTTP_PROXY in environ else None
       if proxy is not None:
           del environ[_HTTP_PROXY]
       r = func(*args, **kwargs)
       if proxy is not None:
           environ[_HTTP_PROXY] = proxy
       return r
   return func_wrapper

if __name__ == '__main__':
    pass