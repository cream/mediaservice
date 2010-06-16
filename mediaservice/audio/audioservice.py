#!/usr/bin/env python

import pymongo

import cream.ipc
import cream.extensions

from crawler import crawl

MUSIC_DIR = '/mnt/Daten/Musik'

@cream.extensions.register
class AudioExtension(cream.extensions.Extension, cream.ipc.Object):
    def __init__(self, *args, **kwargs):
        cream.extensions.Extension.__init__(self, *args, **kwargs)
        cream.ipc.Object.__init__(self,
            'org.cream.mediaservice',
            '/org/cream/Mediaservice/Audio'
        )

        self.document = pymongo.Connection().mediaservice.audio

    @cream.ipc.method(interface='org.cream.Mediaservice.Audio')
    def update_library(self):
        crawl(MUSIC_DIR)

    @cream.ipc.method('', 'aa{sv}', interface='org.cream.Mediaservice.Audio')
    def list_tracks(self):
        return [song for song in self.document.find()]


    @cream.ipc.method('a{sv}', 'aa{sv}', interface='org.cream.Mediaservice.Audio')
    def query(self, query):
        '''returns a list containing query results
            query: dict. e.g. {'artist': 'Elvis Presly', 'title': 'rock around the clock'}
        '''
        return [song for song in self.document.find(query)]


    @cream.ipc.method('s', '')
    def play_track_by_path(self, path):
        self.player.play(Track.get_absolute_path(path))


    @cream.ipc.method
    def pause_playback(self):
        self.player.pause()


    @cream.ipc.method
    def stop_playback(self):
        self.player.stop()


    @cream.ipc.method
    def toggle_playback(self):
        self.player.toggle()

