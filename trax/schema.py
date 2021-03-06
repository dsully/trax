"""
  ORM definition & engine bits for SQLAlchemy
"""

import os

from sqlalchemy import Column, Integer, String, Text, Boolean, Float, SmallInteger, Unicode, UnicodeText, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, ColumnProperty
from sqlalchemy.orm.mapper import class_mapper
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Metadata(Base):
  __tablename__     = 'metadata'

  name  = Column(String(64), primary_key=True)
  value = Column(Text)

class Track(Base):
  __tablename__              = 'tracks'

  id                         = Column(Integer, primary_key=True)
  filename                   = Column(Unicode(256), index=True)
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

  genre                      = Column(Unicode(256), index=True)
  grouping                   = Column(Unicode(256), index=True)
  date                       = Column(String(10), index=True)
  compilation                = Column(Boolean, index=True)
  tracknumber                = Column(SmallInteger)
  tracktotal                 = Column(SmallInteger)
  bpm                        = Column(SmallInteger, index=True)
  publisher                  = Column(Unicode(128))
  isrc                       = Column(String(32))
  releasecountry             = Column(Unicode(32))
  barcode                    = Column(String(32))
  lyrics                     = Column(UnicodeText)
  asin                       = Column(String(16))
  media                      = Column(String(16))
  catalognumber              = Column(String(64))

  acoustid_id                = Column(String(64), index=True)
  acoustid_fingerprint       = Column(Text)

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

  replaygain_album_gain      = Column(String(16))
  replaygain_album_peak      = Column(Float)
  replaygain_track_gain      = Column(String(16))
  replaygain_track_peak      = Column(Float)

  url_discogs_release_site   = Column(String(256))
  url_lyrics_site            = Column(String(256))
  url_wikipedia_release_site = Column(String(256))

  discnumber                 = Column(SmallInteger)
  disctotal                  = Column(SmallInteger)
  cover_file                 = Column(Unicode(256), index=True)

  def attribute_names(self):
    """
      Return a list of the column properties for this object.

      :rtype: list
    """

    return [prop.key for prop in class_mapper(self.__class__).iterate_properties if isinstance(prop, ColumnProperty)]

  def filename_for_destination(self, source_dir, dest_dir, extension):
    """
      Return the destination filename for a given codec.

      :rtype: str
    """

    src_file = self.filename
    dst_file = src_file.replace(os.path.normpath(source_dir), os.path.normpath(dest_dir))
    dst_file = os.path.splitext(dst_file)[0] + '.' + extension

    return dst_file

def get_db_session():
  """
    Return a SQLAlchemy session object.
  """

  db_path = os.path.expanduser('~/.trax/trax.db')

  if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

  engine  = create_engine('sqlite:///%s' % db_path, echo=False)

  Base.metadata.create_all(engine)
  #engine  = create_engine('mysql://trax:trax@localhost/trax?unix_socket=/usr/local/var/mysql/mysql.sock', echo=False)

  session    = scoped_session(sessionmaker(bind=engine))
  Base.query = session.query_property()

  return session
