#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
# wip TableTop Simulator json parser
# Copyright (C) 2020  Chris Clark

import glob
import logging
import os
import sys

try:
    #raise ImportError()
    # Python 2.6+
    import json
except ImportError:
    #raise ImportError()
    # from http://code.google.com/p/simplejson
    import simplejson as json


logging.basicConfig() ## NO debug, no info. But logs warnings
log = logging.getLogger("mylogger")
log.setLevel(logging.DEBUG)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        game_dirname = argv[1]
    except IndexError:
        game_dirname = os.path.join(os.environ['USERPROFILE'], 'Documents', 'My Games', 'Tabletop Simulator', 'Mods', 'Workshop')

    log.info('game_dirname %r', game_dirname)
    
    filename = os.path.join(game_dirname, 'WorkshopFileInfos.json')
    f = open(filename, 'rb')
    workshop = json.load(f)
    log.info('read complete, workshop len %r', len(workshop))
    f.close()
    for counter, filename in enumerate(glob.glob(os.path.join(game_dirname, '*.json'))):
        log.info('game_dirname %r', filename)
        if filename.endswith('WorkshopFileInfos.json'):
            continue
        f = open(filename, 'rb')
        data = json.load(f)
        #data = f.read()
        log.info('read complete, len %r', len(data))
        f.close()
        log.info('game %r', data['SaveName'])
        log.info('game %r', data['GameMode'])
        game_id = os.path.basename(filename).replace('.json', '')  # dumb split extn
        game_id = int(game_id)  # assume no leading zeroes
        log.info('game_id %r', game_id)
        log.info('https://steamcommunity.com/sharedfiles/filedetails/?id=%d', game_id)
        tmp_names = glob.glob(os.path.join(game_dirname, str(game_id)+'.*'))
        #log.info('tmp_names %r', tmp_names)
        tmp_names = [os.path.basename(x) for x in tmp_names]
        #log.info('tmp_names %r', tmp_names)
        tmp_names.remove('%d.json' % game_id)
        assert len(tmp_names) == 1
        log.info('game image filename %r', tmp_names[0])

    log.info('counter %r', counter)
    log.info('workshop len %r', len(workshop))  # NOTE seeig dupes in here, nt sure if this explains all count differences though

    return 0

if __name__ == "__main__":
    sys.exit(main())
