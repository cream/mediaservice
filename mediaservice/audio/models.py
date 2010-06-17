#!/usr/bin/env python


class Track(object):
    _fields = (
        'path', 'title', 'artist', 'album',
        'genre', 'year', 'length', 'rating'
    )
    def __init__(self, **kwargs):
        for attr in Track._fields:
            setattr(self, attr, kwargs.pop(attr, None))

        if kwargs:
            raise TypeError("%s.__init__ got unexpected keyword arguments %s"
                            % (type(self).__name__, ', '.join(kwargs.iterkeys())))

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)

    def to_dict(self):
        """ Returns a dict/JSON representation of the Track. """
        return dict(
            (attr, getattr(self, attr)) for attr in Track._fields
        )
