#!/usr/bin/env python
import re

import cream.ipc
import cream.extensions

from crawler import crawl

def mongodb_to_dbus_dict(dict_):
    dict_['_id'] = unicode(dict_['_id'])
    return dict_

@cream.extensions.register
class AudioExtension(cream.extensions.Extension, cream.ipc.Object):

    __ipc_signals__ = {
        'library_updated': ('', 'org.cream.Mediaservice.Audio')
    }

    def __init__(self, database):
        cream.extensions.Extension.__init__(self, None)
        cream.ipc.Object.__init__(self,
            'org.cream.mediaservice',
            '/org/cream/Mediaservice/Audio'
        )
        self.collection = database.audio


    @cream.ipc.method('s', interface='org.cream.Mediaservice.Audio')
    def update_library(self, path):
        crawl(self.collection.tracks, path)
        self.emit_signal('library_updated')

    @cream.ipc.method('', 'aa{sv}', interface='org.cream.Mediaservice.Audio')
    def list_tracks(self):
        return map(mongodb_to_dbus_dict, self.collection.tracks.find())

    @cream.ipc.method('a{sv}', 'aa{sv}', interface='org.cream.Mediaservice.Audio')
    def query(self, query, ignorecase=False):
        if ignorecase:
            for key, value in query.iteritems():
                if isinstance(value, basestring):
                    query[key] = re.compile(value, re.IGNORECASE)

        return map(mongodb_to_dbus_dict, self.collection.tracks.find(query))

    @cream.ipc.method('s', 'aa{sv}', interface='org.cream.Mediaservice.Audio')
    def query_all(self, querystring):
        #query every key in the db, will first work with mongodb 1.5.3
        return map(mongodb_to_dbus_dict, self.collection.tracks.find({ '$or' : [
                                            {'artist': querystring},
                                            {'title': querystring},
                                            {'album': querystring},
                                            {'genre': querystring},
                                            {'year': querystring} ]}
                    ))

    @cream.ipc.method('sa{sv}', '', interface='org.cream.Mediaservice.Audio')
    def update_track(self, _id, track_new):
        self.collection.update({'_id': _id}, {'$set': track_new})

    @cream.ipc.method('s', '', interface='org.cream.Mediaservice.Audio')
    def remove_track(self, _id):
        self.collection.remove(_id)
