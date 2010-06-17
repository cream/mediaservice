#!/usr/bin/env python

import cream.ipc
import cream.extensions

import re

from crawler import crawl

@cream.extensions.register
class AudioExtension(cream.extensions.Extension, cream.ipc.Object):

    __ipc_signals__ = {
        'library_updated': ('', 'org.cream.Mediaservice.Audio')
        }


    def __init__(self, *args, **kwargs):
        cream.extensions.Extension.__init__(self, *args, **kwargs)
        cream.ipc.Object.__init__(self,
            'org.cream.mediaservice',
            '/org/cream/Mediaservice/Audio'
        )

        self.collection = args[0].audio

    @cream.ipc.method('s', interface='org.cream.Mediaservice.Audio')
    def update_library(self, path):
        crawl(self.collection.tracks, path)
        self.emit_signal('library_updated')


    @cream.ipc.method('', 'aa{sv}', interface='org.cream.Mediaservice.Audio')
    def list_tracks(self):
        tracks = []
        for track in self.collection.tracks.find():
            tracks.append(format_id(track))
        return tracks


    @cream.ipc.method('', 'aa{sv}', interface='org.cream.Mediaservice.Audio')
    def query(self, query):
        for key in query.keys():
            query[key] = re.compile(query[key], re.IGNORECASE)

        tracks = []
        for track in self.collection.tracks.find(query):
            tracks.append(format_id(track))
        return tracks



def format_id(dict_):
    dict_['_id'] = str(dict_['_id'])
    return dict_
