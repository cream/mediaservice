#!/usr/bin/env python

import pymongo

import cream
import cream.ipc

class Mediaservice(cream.Module, cream.ipc.Object):
    extension_interface = None

    def __init__(self):

        cream.Module.__init__(self)
        cream.ipc.Object.__init__(self,
            'org.cream.media',
            '/org/cream/Media'
        )

        self.database = pymongo.Connection().mediaservice
        self.audioservice = self.extension_manager.load_by_name('Audioservice', self)


if __name__ == '__main__':
    Mediaservice().main()
