#!/usr/bin/env python

import cream.ipc
import cream.extensions

from crawler import crawl

import re
from pymongo.objectid import ObjectId

def convert_objectid(dict_):
    object_id = dict_.get('_id')
    if object_id is not None:
        if isinstance(object_id, basestring):
            dict_['_id'] = ObjectId(object_id)
        else:
            dict_['_id'] = unicode(object_id)
    return dict_

@cream.extensions.register
class AudioExtension(cream.extensions.Extension, cream.ipc.Object):

    __ipc_signals__ = {
        'library_updated': ('', 'org.cream.MediaService.Audio')
    }

    def __init__(self, extension_interface):
        cream.extensions.Extension.__init__(self, extension_interface)
        cream.ipc.Object.__init__(self,
            'org.cream.mediaservice',
            '/org/cream/MediaService/Audio'
        )
        self.document = extension_interface.database.audio.tracks

    @cream.ipc.method('s')
    def update_library(self, path):
        crawl(self.document, path)
        self.emit_signal('library_updated')

    @cream.ipc.method('a{sv}b', 'aa{sv}')
    def query(self, query, ignorecase):
        if ignorecase:
            for key, value in query.iteritems():
                if isinstance(value, basestring):
                    query[key] = re.compile(value, re.IGNORECASE)

        return map(convert_objectid, self.document.find(query))

    @cream.ipc.method('a{sv}')
    def update_or_add(self, track):
        track = convert_objectid(track)
        self.document.save(track)

    @cream.ipc.method('s')
    def remove_track(self, _id):
        self.document.remove(_id)
