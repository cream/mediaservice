#!/usr/bin/env python

import pymongo

import cream
import cream.ipc

class Mediaservice(cream.Module, cream.ipc.Object):
    def __init__(self):
        self.extension_api = {}

        cream.Module.__init__(self)
        cream.ipc.Object.__init__(self,
            'org.cream.mediaservice',
            '/org/cream/Mediaservice'
        )

        self.db = pymongo.Connection().mediaservice
        self.audioservice = self.extension_manager.load_by_name('Audioservice', self.db)


if __name__ == '__main__':
    Mediaservice().main()
