#!/usr/bin/env python

from collections import defaultdict
from pymongo.objectid import ObjectId

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

def build_tree(tracks, convert_none_to_empty_string=False):
    if convert_none_to_empty_string:
        _ = lambda x: x if x is not None else ''
    else:
        _ = lambda x: x
    tree = defaultdict(lambda: defaultdict(dict))

    for track in tracks:
        track = convert_objectid(track)
        artist = _(track['artist'])
        album = _(track['album'])
        title = _(track['title'])

        if title not in tree[artist][album]:
            # XXX: what do with two tracks with the same name?
            tree[artist][album][title] = {
                'id'      : _(track['_id']),
                'path'    : _(track['path']),
                'genre'   : _(track['genre']),
                'rating'  : _(track['rating']),
                'duration': _(track['duration']),
                'artist': _(track['artist']),
                'album': _(track['album']),
                'title': _(track['title']),
                'tracknumber': _(track['tracknumber']),
            }

    return tree
