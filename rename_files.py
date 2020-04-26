#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
# wip TableTop Simulator json parser
# Copyright (C) 2018  Chris Clark
"""rename files based on file type
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

import glob
import logging
import mimetypes
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

import magic  # TODO consider using https://github.com/clach04/magic-fork


try:
    basestring
except NameError:
    basestring = str

logging.basicConfig() ## NO debug, no info. But logs warnings
log = logging.getLogger("mylogger")
log.setLevel(logging.DEBUG)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        dirname = argv[1]
    except IndexError:
        dirname = '.'
    filename_pattern = os.path.join(dirname, '*')
    for filename in glob.glob(filename_pattern):
        log.info('filename %r', filename)
        if os.path.isfile(filename):
            f = open(filename, 'rb')
            data = f.read(8192)
            log.info('%r read complete, len %r', filename, len(data))
            f.close()
            mime_type = magic.whatis(data)
            if mime_type == 'image/x-png':
                mime_type = 'image/png'
            file_extn = mimetypes.guess_extension(mime_type)
            print(mime_type)
            print(file_extn)
            if file_extn:
                os.rename(filename, filename + file_extn)
        else:
            log.info('%r NOT A FILE', filename)

    return 0

if __name__ == "__main__":
    sys.exit(main())

