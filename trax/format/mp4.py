import logging
import os

import mutagen.mp4
from mutagen.mp4 import MP4Cover

from trax.format.base import Base
from trax.soundcheck import replay_gain_to_soundcheck

log = logging.getLogger(__name__)

class MP4(Base):

  attributes = {
    '\xa9nam': 'title',
    '\xa9alb': 'album',
    '\xa9ART': 'artist',
    '\xa9cmt': 'comment',
    '\xa9day': 'date',
    '\xa9gen': 'genre',
    '\xa9grp': 'grouping',
    'aART'   : 'albumartist',
    '\xa9wrt': 'composer',
    '\xa9lyr': 'lyrics',
    'soal'   : 'albumsort',
    'soar'   : 'artistsort',
    'soaa'   : 'albumartistsort',
    'soco'   : 'composersort',
    'tmpo'   : 'bpm',
  }

  def is_up_to_date(self):
    try:
      if self.track.mtime == self.tags["----:com.sully.flac2mp4:flacmtime"][0]:
        return True
    except KeyError:
      pass

    return False

  def extract_artwork(self):

    basename = os.path.dirname(self.filename)
    tags     = mutagen.mp4.MP4(self.filename)

    if "covr" in tags and len(tags["covr"]) > 0:

      if tags["covr"][0].imageformat == MP4Cover.FORMAT_JPEG:
        cover_file = os.path.join(basename, "cover.jpg")
      else:
        cover_file = os.path.join(basename, "cover.png")

      # Only write out if we've changed.
      if os.path.exists(cover_file):
        if self.track.mtime <= int(os.stat(cover_file).st_mtime):
          return cover_file

      try:
        with open(cover_file, "wb") as fh:
          fh.write(tags["covr"][0])

      except IOError, e:
        print "Couldn't write to file (%s): %s" % (cover_file, e)
        return None

      return cover_file

  def write_metadata(self, filename, force=False):

    # MP4 needs these attributes as TXXX.
    for value in ('original album', 'original_artist', 'original_year'):
      self.txxx[value.upper().replace('_', ' ')] = value

    track = self.track

    log.debug("Writing metadata for: %s", filename)

    if os.path.exists(filename) is False:
      log.warn("Couldn't find MP4 file!: %s", filename)
      return None

    self.tags = mutagen.mp4.MP4(filename)

    if not force and self.is_up_to_date():
      log.debug('Up to date: "%s"' % filename)
      return None

    # Clear out any old data.
    self.tags.clear()

    # Basics first.
    for atom, key in self.attributes.iteritems():

      if hasattr(track, key):
        value = getattr(track, key, None)

        log.debug("Trying: key: %s (%s)", key, value)

        if value:
          self.tags[atom] = value.encode('utf-8')

    # Hack alert.. not sure how better to "detect" this.
    if track.genre:
      for genre in list(track.genre):
        if genre in self.gapless:
          self.tags["pgap"] = True

    if track.compilation:
      self.tags["cpil"] = True

    if track.tracknumber and track.tracktotal:
      self.tags["trkn"] = [(track.tracknumber, track.tracktotal)]

    elif track.tracknumber:
      self.tags["trkn"] = [(track.tracknumber, 0)]

    # Convert RG tags into iTunes SoundCheck
    # TODO: Find what tags aacgain uses as well.
    if track.replaygain_album_gain:
      self.tags['----:com.apple.iTunes:iTunNORM'] = replay_gain_to_soundcheck(track.replaygain_album_gain, track.replaygain_album_peak)

    elif track.replaygain_track_gain:
      self.tags['----:com.apple.iTunes:iTunNORM'] = replay_gain_to_soundcheck(track.replaygain_track_gain, track.replaygain_track_peak)

    #
    if track.discnumber and track.disctotal:
      try:
        self.tags["disk"] = [(track.discnumber, track.disctotal)]
      except ValueError:
        pass

    elif track.disctotal:
      self.tags["disk"] = [(track.disctotal, track.disctotal)]

    # Artwork time..
    if track.cover_file and os.path.exists(track.cover_file):

      with open(track.cover_file, 'rb') as fh:

        if track.cover_file.endswith(".png"):
          self.tags["covr"] = [ MP4Cover(fh.read(), MP4Cover.FORMAT_PNG) ]
        elif track.cover_file.endswith(".jpg"):
          self.tags["covr"] = [ MP4Cover(fh.read(), MP4Cover.FORMAT_JPEG) ]

    # Always add the check & time stamp for next time.
    if track.checksum:
      self.tags['----:com.sully.flac2mp4:checksum'] = str(track.checksum)

    self.tags['----:com.sully.flac2mp4:flacmtime'] = str(track.mtime)

    # Convert all user defined tags.
    for tag, attribute in self.txxx.iteritems():

      if getattr(track, attribute, None):
        self.tags['----:com.apple.iTunes:' + tag] = getattr(track, attribute).encode('utf-8')

    try:
      self.tags.save(filename)
    except Exception, e:
      log.warn("Couldn't save file %s: %s", filename, e)
