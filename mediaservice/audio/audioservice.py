import cream.ipc
import cream.extensions
from mediaservice.audio.models import Track

@cream.extensions.register
class AudioExtension(cream.extensions.Extension, cream.ipc.Object):
    def __init__(self, *args, **kwargs):
        cream.extensions.Extension.__init__(self, *args, **kwargs)
        cream.ipc.Object.__init__(self,
            'org.cream.mediaservice',
            '/org/cream/Mediaservice/Audio'
        )

    @cream.ipc.method
    def update_library(self):
        from mediaservice.audio.crawler import crawl
        from mediaservice.audio import MUSIC_DIR
        crawl(MUSIC_DIR)

    @cream.ipc.method('', 'aa{sv}')
    def list_tracks(self):
        return [track.to_dict() for track in Track.query.all()]

    @cream.ipc.method('i', '')
    def play_track_by_id(self, id):
        self.player.play(Track.query.filter_by(id=id).one().absolute_path)

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
