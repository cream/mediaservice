#!/usr/bin/env python

from cream.util import walkfiles
import mutagen
import pymongo

KEYS = ['title', 'artist', 'album', 'genre', 'year']

def crawl(path):
    
    connection = pymongo.Connection()
    document = connection.mediaservice.audio

    for file_ in walkfiles(path):
        if not document.find_one({'path': file_}):
            track = Track.from_file(file_)
            if track:
                print file_
                document.insert(track.to_json())
        

class Track(object):
    def __init__(self, title, artist, album, genre, year, length, path, rating):
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year
        self.length = length
        self.path = path
        self.rating = rating
        

    def to_json(self):
        '''returns a JSON representation of the Track'''

        return {'title': self.title,
                'artist': self.artist,
                'album': self.album,
                'genre': self.genre,
                'year': self.year,
                'length': self.length,
                'path': self.path,
                'rating': self.rating
        }
    
    @classmethod
    def from_file(cls, file_):
        metadata = mutagen.File(file_, easy=True)
        if metadata is None:
            return
        data = dict()
        for key in KEYS:
            try:
                data[key] = metadata[key][0]
            except KeyError:
                data[key] = None

        return Track(data['title'],
                    data['artist'],
                    data['album'],
                    data['genre'],
                    data['year'],
                    metadata.info.length,
                    file_,
                    0
        )
        
