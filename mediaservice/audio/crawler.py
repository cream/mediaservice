#!/usr/bin/env python
from future_builtins import map
import mutagen
from os.path import relpath
from cream.util import walkfiles
from util import get_first_item_or_none


def crawl(path, collection):
    for file_ in walkfiles(path):
        metadata = mutagen.File(file_, easy=True)
        if not metadata:
            # not a media file or file not supported. skip.
            continue

        artist, album, title, year, genre, tracknumber = \
            map(lambda key: get_first_item_or_none(metadata.get(key)),
                ('artist', 'album', 'title', 'date', 'genre', 'tracknumber'))
        if tracknumber is not None:
            # 5/12 -> 5
            tracknumber = tracknumber.split('/')[0]
        duration = metadata.info.length
        rating = 0

        track = {
            'artist': artist,
            'album': album,
            'title': title,
            'year': year,
            'genre': genre,
            'tracknumber': tracknumber,
            'duration': duration,
            'rating': rating,
            'path': file_
        }
        collection.save(track)

