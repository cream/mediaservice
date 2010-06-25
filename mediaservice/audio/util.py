#!/usr/bin/env python

def build_tree(tracks):
    tree = {}
    for track in tracks:
        track = convert_objectid(track)
        artist = track['artist']
        album = track['album']
        title = track['title']

        if not tree.has_key(artist):
            tree[artist] = {}

        if not tree[artist].has_key(album):
            tree[artist][album] = {}

        if not tree[artist][album].has_key(title):
            tree[artist][album][title] = {
                'rating': track['rating'], 
                'duration': track['duration'], 
                'genre': track['genre'], 
                'path': track['path'], 
                'id': track['_id']
            }

    return tree


def convert_objectid(dict_):
    object_id = dict_.get('_id')
    if object_id is not None:
        if isinstance(object_id, basestring):
            dict_['_id'] = ObjectId(object_id)
        else:
            dict_['_id'] = unicode(object_id)
    return dict_
