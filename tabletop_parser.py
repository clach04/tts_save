#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
# wip TableTop Simulator json parser
# Copyright (C) 2018  Chris Clark
"""goldenfleece - its what JSON was seeking.....
"""

import base64

# json support, TODO consider http://pypi.python.org/pypi/omnijson
try:
    #raise ImportError()
    # Python 2.6+
    import json
except ImportError:
    try:
        #raise ImportError()
        # from http://code.google.com/p/simplejson
        import simplejson as json
    except ImportError:
        json = None

import logging
import os
import sys
try:
    # Assume Python 3.x
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
except ImportError:
    # Probably Python2
    from urllib import urlencode
    from urllib2 import Request, urlopen
    from urllib2 import URLError, HTTPError
import warnings


try:
    basestring
except NameError:
    basestring = str

logging.basicConfig() ## NO debug, no info. But logs warnings
log = logging.getLogger("mylogger")
log.setLevel(logging.DEBUG)


def naive_dump_json(x, indent=None):
    """dumb not safe!
    Works for the purposes of this specific script as quotes never
    appear in data set.
    
    Parameter indent ignored"""
    warnings.warn('about to dump rough read_json')
    assert isinstance(x, dict)
    # could use pprint for the purposes of this specific script
    return repr(x).replace("'", '"')

def naive_load_json(x):
    """dumb not safe! Works for the purposes of this specific script
    
    Has one advantage over real json/simpljson libs, it handles firefox
    bookmarks.json exports
    """
    warnings.warn('about to evaluate/execute potentially unsafe code (read_json)')
    null = None
    return eval(x)


if json is None:
    dump_json = naive_dump_json
    load_json = naive_load_json
else:
    dump_json = json.dumps
    load_json = json.loads

log.info('Python %s on %s', sys.version, sys.platform)  # TODO make this info?

def get_any_url(url, filename=None, force=False):
    filename = filename or 'tmp_file.html'
    ## cache it
    if force or not os.path.exists(filename):
        log.debug('getting web page %r', url)
        page_filehandle = urlopen(url)
        # TODO use mime type to determine file extension; page_filehandle.getheader('Content-Type')
        page = page_filehandle.read()
        page_filehandle.close()
        f = open(filename, 'wb')
        f.write(page)
        f.close()
    else:
        log.debug('getting file %r', filename)
        f = open(filename, 'rb')
        page = f.read()
        f.close()

    return page


def find_in_obj(obj, condition_func, path=None):

    if path is None:
        path = []    

    # In case this is a list
    if isinstance(obj, list):
        for index, value in enumerate(obj):
            new_path = list(path)
            new_path.append(index)
            for result in find_in_obj(value, condition_func, path=new_path):
                yield result 

    # In case this is a dictionary
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = list(path)
            new_path.append(key)
            for result in find_in_obj(value, condition_func, path=new_path):
                yield result 

            if condition_func(key, value):
                new_path = list(path)
                new_path.append(key)
                yield new_path 

def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        filename = argv[1]
    except IndexError:
        filename = 'TS_Save_10.json'
    log.info('filename %r', filename)
    f = open(filename, 'rb')
    data = f.read()
    log.info('read complete, len %r', len(data))
    f.close()

    """Load json and then look for any value that starts with 'http' (so no ftp support).
    Then dump to disk, based on the key (path) name.

    TODO Consider using jsonpath, looks like $..FaceURL and $..BackURL would be needed as minimum
    TODO Consider re-writting json to access downloaded file(s).
    TODO Consider re-writting json with embedded base64 encoded values.
    """

    #data data de-encoding..... from UTF8
    tmp_data = load_json(data)
    log.debug('load complete')
    pretty_json = dump_json(tmp_data, indent=4)
    #print(pretty_json)
    log.debug('dump complete')
    print(tmp_data["TableURL"])
    """
    # appears to be a black image
    print(tmp_data["DrawImage"])
    print(base64.decodestring(tmp_data["DrawImage"]))
    f = open('DrawImage.png', 'wb')
    f.write(base64.decodestring(tmp_data["DrawImage"]))
    f.close()
    """

    """
    for key, value in tmp_data.items():
        print(key, value)
    """

    print('-' * 65)
    def check_value_is_url(k, v):
        #print(k,v)
        if isinstance(v, basestring):
            return v.startswith('http')  # super dumb
        return False

    url_dict = {}
    counter = 0
    for item in find_in_obj(tmp_data, check_value_is_url):
        counter = counter + 1  # fixme should have used enumerate
        print(item)
        temp_filename = '.'.join(map(str, item))
        tmp_x = tmp_data
        for i in item:
            tmp_x = tmp_x[i]
        log.info((temp_filename, tmp_x))
        get_any_url(tmp_x, filename=temp_filename)
        #url_dict[temp_filename] = tmp_x
        url_dict[tmp_x] = temp_filename
    #print(tmp_data['ObjectStates'][4]['CustomDeck']['1']['FaceURL'])
    print(len(url_dict))
    print(counter)
    """
    73
    73

    38  # uniq urls
    73
    """

    return 0

if __name__ == "__main__":
    sys.exit(main())



