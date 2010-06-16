import cream.ipc

audio = cream.ipc.get_object('org.cream.mediaservice', 
                                    '/org/cream/Mediaservice/Audio')

print audio.list_tracks()
