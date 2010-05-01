from elixir import Field, Unicode, Float, Integer, SmallInteger, \
                   ManyToMany, OneToMany, ManyToOne
from elixir import using_options
from ..modelbase import MediaItem, ModelBase, DEFAULT_STRING_SIZE


class TypeNotSupported(TypeError):
    pass

def get_first(dict_, key):
    item = dict_.get(key)
    if item is not None:
        return item[0]

class Track(MediaItem):
    using_options(inheritance='multi')

    title = Field(Unicode(DEFAULT_STRING_SIZE))
    length = Field(Float)
    year = Field(SmallInteger)
    genre = Field(Unicode(DEFAULT_STRING_SIZE))
    artist = Field(Unicode())
    album = Field(Unicode(DEFAULT_STRING_SIZE))
    album_cover = Field(Unicode)


    @classmethod
    def from_file(cls, file_):
        import mutagen

        metadata = mutagen.File(file_, easy=True)
        if metadata is None:
            raise TypeNotSupported("File format of %s is not supported" % file_)

        return Track(
            title   = get_first(metadata, 'title'),
            year    = get_first(metadata, 'year'),
            artist  = get_first(metadata, 'artist'),
            album   = get_first(metadata, 'album'),
            genre   = get_first(metadata, 'genre'),
            length  = metadata.info.length
        )
