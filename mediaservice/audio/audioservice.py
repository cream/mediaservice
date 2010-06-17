#!/usr/bin/env python

import cream.ipc
import cream.extensions

import re

@cream.extensions.register
class AudioExtension(cream.extensions.Extension, cream.ipc.Object):
    def __init__(self, *args, **kwargs):
        cream.extensions.Extension.__init__(self, *args, **kwargs)
        cream.ipc.Object.__init__(self,
            'org.cream.mediaservice',
            '/org/cream/Mediaservice/Audio'
        )

        self.collection = args[0].audio

    @cream.ipc.method(interface='org.cream.Mediaservice.Audio')
    def list_tracks(self):
        return [track for track in self.collection.find()]

    @cream.ipc.method(interface='org.cream.Mediaservice.Audio')
    def query(self, query):
        for key in query.keys():
            query[key] = re.compile(query[key], re.IGNORECASE)

        return [track for track in self.collection.find(query)]
