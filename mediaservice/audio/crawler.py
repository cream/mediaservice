#!/usr/bin/env python

from cream.util import walkfiles
import mutagen

def crawl(path):
    for file_ in walkfiles(path):
        if not document.find_one({'path': file_}):
            track = Track.from_file(file_)
            if track:
                print file_
                document.insert(track.to_dict())
