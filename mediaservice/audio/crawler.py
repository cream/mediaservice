from ..modelbase import session
from models import Track, TypeNotSupported
from cream.util import walkfiles


def crawl(path):
    i = 0
    for file_ in walkfiles(path):
        i += 1
        if i % 10 == 0:
            print i
        try:
            session.add(Track.from_file(file_))
        except TypeNotSupported:
            pass

    session.commit()
