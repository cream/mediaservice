#!/usr/bin/env python

import mutagen
from os.path import relpath
from cream.util import walkfiles


def get_tracknumber(data):
    
    tracknumber = data.get('tracknumber', [None])[0]
    if tracknumber:
        return tracknumber.split('/')[0]
    else:
        return '1'


def crawl(path, collection):
    for file_ in walkfiles(path):
        metadata = mutagen.File(file_, easy=True)
        if not metadata:
            continue
            #file not supported

        artist = metadata.get('artist', [''])[0]
        album = metadata.get('album', [''])[0]
        title = metadata.get('title', [''])[0]
        year = metadata.get('year', [''])[0]
        genre = metadata.get('genre', [''])[0]
        tracknumber = get_tracknumber(metadata)
        duration = metadata.info.length
        rating = 0

        track = {'artist': artist,
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

