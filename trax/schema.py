from sqlalchemy import Column, Integer, String, Text, Boolean, LargeBinary, Float, SmallInteger, Unicode, UnicodeText, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, ColumnProperty
from sqlalchemy.orm.mapper import class_mapper
from sqlalchemy.ext.declarative import declarative_base

#engine  = create_engine('sqlite:////Users/dsully/dev/audio/test.db', echo=False)
engine  = create_engine('mysql://dsully:insecure@localhost/audio_metadata', echo=False)
Base    = declarative_base(bind=engine)

class Metadata(Base):
  __tablename__     = 'metadata'

  name  = Column(String(64), primary_key=True)
  value = Column(Text)

class Track(Base):
  __tablename__              = 'tracks'

  id                         = Column(Integer, primary_key=True)
  filename                   = Column(Unicode(512), index=True)
  mtime                      = Column(Integer, index=True)
  filetype                   = Column(String(4), index=True)
  checksum                   = Column(String(128), index=True)

  title                      = Column(Unicode(256), index=True)
  album                      = Column(Unicode(256), index=True)
  albumsort                  = Column(Unicode(256))
  artist                     = Column(Unicode(256), index=True)
  artistsort                 = Column(Unicode(256))
  albumartist                = Column(Unicode(256), index=True)
  albumartistsort            = Column(Unicode(256))
  composer                   = Column(Unicode(256), index=True)
  composersort               = Column(Unicode(256))

  original_album             = Column(Unicode(256), index=True)
  original_artist            = Column(Unicode(256), index=True)
  original_year              = Column(String(16), index=True)

  genre                      = Column(String(256), index=True)
  grouping                   = Column(String(256), index=True)
  date                       = Column(String(10), index=True)
  compilation                = Column(Boolean, index=True)
  tracknumber                = Column(SmallInteger)
  tracktotal                 = Column(SmallInteger)
  bpm                        = Column(SmallInteger, index=True)
  publisher                  = Column(Unicode(128))
  isrc                       = Column(String(32))
  releasecountry             = Column(String(32))
  barcode                    = Column(String(32))
  lyrics                     = Column(UnicodeText)
  asin                       = Column(String(16))
  media                      = Column(String(16))
  catalognumber              = Column(String(64))

  musicbrainz_albumid        = Column(String(64))
  musicbrainz_albumartistid  = Column(String(64))
  musicbrainz_albumstatus    = Column(String(32))
  musicbrainz_albumtype      = Column(String(32))
  musicbrainz_artistid       = Column(String(64))
  musicbrainz_discid         = Column(String(64))
  musicbrainz_trackid        = Column(String(64))
  musicbrainz_trmid          = Column(String(64))
  musicip_fingerprint        = Column(Text)
  musicip_puid               = Column(String(128), index=True)

  replaygain_album_gain      = Column(String(16), index=True)
  replaygain_album_peak      = Column(Float, index=True)
  replaygain_track_gain      = Column(String(16), index=True)
  replaygain_track_peak      = Column(Float, index=True)

  url_discogs_release_site   = Column(String(256))
  url_lyrics_site            = Column(String(256))
  url_wikipedia_release_site = Column(String(256))

  discnumber                 = Column(SmallInteger)
  disctotal                  = Column(SmallInteger)
  cover_file                 = Column(Unicode(512), index=True)

  def attribute_names(self):
    """ Return a list of the column properties for this object. """

    return [prop.key for prop in class_mapper(self.__class__).iterate_properties if isinstance(prop, ColumnProperty)]

session = scoped_session(sessionmaker(bind=engine))

Base.metadata.create_all()
Base.query = session.query_property()
