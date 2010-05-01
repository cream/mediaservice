from elixir import Entity, Field, Integer, Unicode, \
                   DateTime, SmallInteger, ManyToMany, \
                   using_options
from elixir import session
from sqlalchemy.orm import validates

from datetime import datetime


DEFAULT_STRING_SIZE = 100

class ModelBase(Entity):
    using_options(abstract=True)

    @classmethod
    def get_or_create(cls, **kwargs):
        create_kwargs = kwargs.pop('create_kwargs', dict())
        obj = cls.query.filter_by(**kwargs).first()
        if obj is None:
            kwargs.update(create_kwargs)
            obj = cls(**kwargs)
            session.add(obj)
            session.commit()
        return obj



class MediaItem(ModelBase):
    using_options(abstract=True)

    time_added = Field(DateTime)
    time_edited = Field(DateTime)
    time_used = Field(DateTime)
    use_count = Field(Integer)
    rating = Field(SmallInteger)

    tags = ManyToMany('Tag')

    @validates('rating')
    def validate_rating(self, key, rating):
        assert rating in xrange(5)
        return rating

    def __init__(self, **kwargs):
        kwargs.setdefault('use_count', 0)
        kwargs['time_added'] = datetime.now()
        ModelBase.__init__(self, **kwargs)

class Tag(ModelBase):
    name = Field(Unicode(30), unique=True)


def setup():
    from elixir import metadata, create_all, setup_all
    from audio.models import Track

    DATABASE = 'sqlite:///mediadb.sql'
    DEBUG = True

    metadata.bind = DATABASE
    metadata.bind.echo = DEBUG

    setup_all()
    create_all()
