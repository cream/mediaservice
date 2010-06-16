#!/usr/bin/env python


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

    def to_dict(self):
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
