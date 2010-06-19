#!/usr/bin/env python

import cream.ipc
import cream.extensions

from crawler import crawl

import re
from pymongo.objectid import ObjectId

def mongodb_to_dbus_dict(dict_):
    dict_['_id'] = unicode(dict_['_id'])
    return dict_

def dbus_to_mongodb_dict(dict_):
    """
    Converts various dbus type subclasses to native Python types.
    (for example, dbus.Int32 -> int)
    """
    for key, value in dict_.iteritems():
        if isinstance(value, float):
            dict_[key] = float(value)
        elif isinstance(value, int):
            dict_[key] = int(value)
    dict_['_id'] = ObjectId(dict_['_id'])
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

        return map(mongodb_to_dbus_dict, self.document.find(query))

    @cream.ipc.method('a{sv}')
    def update_or_add(self, track):
        track = dbus_to_mongodb_dict(track)
        self.document.save(track)

    @cream.ipc.method('s')
    def remove_track(self, _id):
        self.document.remove(_id)
