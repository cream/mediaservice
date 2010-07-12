#!/usr/bin/env python
import re
import cream.ipc
import cream.extensions

import gobject

from crawler import crawl
from util import build_tree, convert_objectid

from pymongo.objectid import ObjectId

import gst

@cream.extensions.register
class AudioExtension(cream.extensions.Extension, cream.ipc.Object):

    def __init__(self, api):

        cream.extensions.Extension.__init__(self, api)
        cream.ipc.Object.__init__(self,
            'org.cream.media',
            '/org/cream/Media/Audio'
        )

        self.api = api

        self.collection = AudioCollection(api)
        self.player = AudioPlayer(api)


class AudioPlayer(cream.ipc.Object):

    __ipc_signals__ = {
        'state_changed': ('a{sv}', 'org.cream.Media.Audio.Player')
    }

    def __init__(self, api):

        cream.ipc.Object.__init__(self,
            'org.cream.media',
            '/org/cream/Media/Audio/Player'
        )

        self.api = api
        self.collection = self.api.database.audio

        self.active_track = None

        self.player = gst.parse_launch('playbin2')

        gobject.timeout_add(100, self.update)


    def update(self):

        if self.active_track:
            track = str(self.active_track['_id'])
        else:
            track = False

        try:
            position = self.player.query_position(gst.FORMAT_TIME)[0] / 1000000000.0
        except:
            position = 0.0

        state = int(self.player.get_state()[1])

        data = {
            'state': state,
            'track': track,
            'position': position
            }

        self.emit_signal('state_changed', data)
        return True


    @cream.ipc.method('s')
    def set_track(self, id):
        self.active_track = self.collection.tracks.find({'_id': ObjectId(id)})[0]

        self.player.set_state(gst.STATE_NULL)
        self.player.set_property('uri', 'file://{0}'.format(self.active_track['path']))

        self.update()


    @cream.ipc.method
    def play(self):
        self.player.set_state(gst.STATE_PLAYING)
        self.update()


    @cream.ipc.method
    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)
        self.update()


class AudioCollection(cream.ipc.Object):

    __ipc_signals__ = {
        'library_updated': ('', 'org.cream.Media.Audio.Player')
    }

    def __init__(self, api):

        cream.ipc.Object.__init__(self,
            'org.cream.media',
            '/org/cream/Media/Audio/Collection'
        )

        self.api = api
        self.collection = self.api.database.audio


    @cream.ipc.method('s')
    def update_library(self, path):
        crawl(path, self.collection.tracks)
        self.emit_signal('library_updated')

    @cream.ipc.method('a{sv}b', 'a{sa{sa{sa{sv}}}}')
    def query(self, query, ignorecase):
        if '_id' in query:
            query = convert_objectid(query)
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
