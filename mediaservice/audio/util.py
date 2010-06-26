#!/usr/bin/env python
from collections import defaultdict

def get_first_item_or_none(obj):
    return obj if obj is None else obj[0]

def convert_objectid(dict_):
    object_id = dict_.get('_id')
    if object_id is not None:
        if isinstance(object_id, basestring):
            dict_['_id'] = ObjectId(object_id)
        else:
            dict_['_id'] = unicode(object_id)
    return dict_

def build_tree(tracks):
    tree = defaultdict(lambda: defaultdict(dict))

    for track in tracks:
        track = convert_objectid(track)
        artist = track['artist']
        album = track['album']
        title = track['title']

        if title not in tree[artist][album]:
            # XXX: what do with two tracks with the same name?
            tree[artist][album][title] = {
                'rating': track['rating'],
                'duration': track['duration'],
                'genre': track['genre'],
                'path': track['path'],
                'id': track['_id']
            }

    return tree
