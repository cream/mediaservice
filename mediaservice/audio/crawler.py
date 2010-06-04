from cream.util import walkfiles
from mediaservice.modelbase import session
from mediaservice.utils import TypeNotSupported
from mediaservice.audio.models import Track


def crawl(path):
    for file_ in walkfiles(path):
        try:
            session.add(Track.from_file(file_))
        except TypeNotSupported, exc:
            print exc

    session.commit()
