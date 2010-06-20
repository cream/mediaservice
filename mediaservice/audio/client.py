#!/usr/bin/env python

import cream.ipc


class Client(object):

    def __init__(self):
        self.audioservice = cream.ipc.get_object('org.cream.mediaservice', 
                                  '/org/cream/MediaService/Audio')

    def update_library(self, path):
        self.audioservice.update_library(path)

    def query(self, query={}, ignorecase=False):
        return self.audioservice.query(query, ignorecase)

    def update_or_add(self, track):
        self.audioservice.update_or_add(track)

    def remove_track(self, _id):
        self.audioservice.remove_track(_id)
