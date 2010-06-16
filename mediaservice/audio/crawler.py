#!/usr/bin/env python

import mutagen
from os.path import relpath

from cream.util import walkfiles
from models import Track

KEYS = ['title', 'artist', 'album', 'genre', 'year']

def crawl(collection, path):
    for file_ in walkfiles(path):
        if collection.find_one({'path': file_}):
            continue
        metadata = mutagen.File(file_, easy=True)
        if not metadata:
            continue
        data = dict()
        for key in KEYS:
            try:
                data[key] = metadata[key][0]
            except KeyError:
                    data[key] = 'Unknown'

        track = Track(data['title'],
                    data['artist'],
                    data['album'],
                    data['genre'],
                    data['year'],
                    metadata.info.length,
                    relpath(file_, path),
                    0 
        )
        collection.insert(track.to_dict())
