#!/usr/bin/env python
import re
import cream.ipc
import cream.extensions

from crawler import crawl
from util import build_tree, convert_objectid

@cream.extensions.register
class AudioExtension(cream.extensions.Extension, cream.ipc.Object):

    __ipc_signals__ = {
        'library_updated': ('', 'org.cream.Media.Audio')
    }

    def __init__(self, extension_interface):
        cream.extensions.Extension.__init__(self, extension_interface)
        cream.ipc.Object.__init__(self,
            'org.cream.media',
            '/org/cream/Media/Audio'
        )

        self.collection = extension_interface.database.audio


    @cream.ipc.method('s')
    def update_library(self, path):
        crawl(path, self.collection.tracks)
        self.emit_signal('library_updated')

    @cream.ipc.method('a{sv}b', 'a{sa{sa{sa{sv}}}}')
    def query(self, query, ignorecase):
        if ignorecase:
            for key, value in query.iteritems():
                if isinstance(value, basestring):
                    query[key] = re.compile(value, re.IGNORECASE)

        return build_tree(self.collection.tracks.find(query),
                          convert_none_to_empty_string=True)

    @cream.ipc.method('a{sv}')
    def update_or_add(self, track):
        track = convert_objectid(track)
        self.collection.tracks.save(track)

    @cream.ipc.method('s')
    def remove_track(self, _id):
        self.collection.tracks.remove(_id)
