#!/usr/bin/env python
from os.path import relpath
from cream.util import walkfiles
import mutagen
from models import Track

def crawl(collection, path, force_update=False):
    for file_ in walkfiles(path):
        if not force_update and collection.find_one({'path': file_}):
            # file already tracked
            continue
        metadata = mutagen.File(file_, easy=True)
        if not metadata:
            # could not parse the file
            continue

        data = dict((k, metadata.get(k, [''])[0]) for k in
                    ('title', 'artist', 'album', 'genre', 'year'))
        data.update({
            'length' : metadata.info.length,
            'rating' : 0,
            'path'   : relpath(file_, path)
        })

        track = Track.from_dict(data)
        collection.insert(track.to_dict())
