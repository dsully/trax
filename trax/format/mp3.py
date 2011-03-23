import logging
import os

import mutagen
import mutagen.id3

from trax.format.base import Base
from trax.soundcheck import replay_gain_to_soundcheck

log = logging.getLogger(__name__)

class MP3(Base):

  attributes = {
    'TIT2': 'title',
    'TALB': 'album',
    'TPE1': 'artist',
    'TPE2': 'albumartist',
    'TCON': 'genre',
    'TIT1': 'grouping',
    'TCOM': 'composer',
    'TDRC': 'date',
    'TSRC': 'isrc',
    'TMED': 'media',
    'TRCK': 'tracknumber',
    'TBPM': 'bpm',
    'TPUB': 'publisher',
    'TSOA': 'albumsort',
    'TSOP': 'artistsort',
    'TSO2': 'albumartistsort',
    'TOAL': 'original_album',
    'TOPE': 'original_artist',
    'TORY': 'original_year',
  }

  def extract_artwork(self):

    basename = os.path.dirname(self.filename)
    tags     = mutagen.File(self.filename)

    if "apic" in tags and len(tags["apic"]) > 0:

      if tags["apic"][0].mime == "image/jpeg":
        cover_file = os.path.join(basename, "cover.jpg")
      else:
        cover_file = os.path.join(basename, "cover.png")

      # Only write out if we've changed.
      if os.path.exists(cover_file):
        if self.track.mtime <= int(os.stat(cover_file).st_mtime):
          return cover_file

      try:
        with open(cover_file, "wb") as fh:
          fh.write(tags["apic"][0].data)

      except IOError, e:
        log.warn("Couldn't write to file (%s): %s", cover_file, e)
        return None

      return cover_file

  def is_up_to_date(self):
    try:
      if self.track.mtime == self.tags["TXXX:flacmtime"][0]:
        return True
    except KeyError:
      pass

    return False

  def set_text_frame(self, frame, value):
    self.tags.add(mutagen.id3.Frames[frame](encoding=3, text=unicode(value)))

  def set_txxx_frame(self, desc, value):
    self.tags.add(mutagen.id3.TXXX(encoding=3, desc=desc, text=unicode(value)))

  def set_replaygain(self, rg_type, gain, peak):
    self.tags.add(mutagen.id3.COMM(encoding=3, lang='eng', desc='iTunNORM', text=replay_gain_to_soundcheck(gain, peak)))

    self.tags.add(mutagen.id3.RVA2(desc=rg_type, channel=1, gain=float(gain.replace(' dB', '')), peak=float(peak)))

    # For foobar and Rockbox
    self.tags.add(mutagen.id3.TXXX(encoding=3, desc='replaygain_%s_gain' % rg_type, text=str(gain)))
    self.tags.add(mutagen.id3.TXXX(encoding=3, desc='replaygain_%s_peak' % rg_type, text=str(peak)))

  def write_metadata(self, filename, force=False):
    track    = self.track

    log.info(filename)

    if os.path.exists(filename) is False:
      log.warn("Couldn't find mp3 file!: %s", filename)
      return None

    try:
      self.tags = mutagen.id3.ID3(filename)
    except mutagen.id3.ID3NoHeaderError:
      log.warn("No ID3 header found; creating a new tag for %s", filename)
      self.tags = mutagen.id3.ID3()

    if not force and self.is_up_to_date():
      log.debug('Up to date: "%s"', filename)
      return None

    if len(self.tags):
      self.tags.delete()

    for frame, prop in self.attributes.iteritems():
      if getattr(track, prop):
        self.set_text_frame(frame, getattr(track, prop))

    # Convert all user defined tags.
    for prop, name in self.txxx.iteritems():
      if hasattr(track, prop) and getattr(track, prop):
        self.set_txxx_frame(name, getattr(track, prop))

    if track.compilation is not None:
      if track.compilation is True:
        self.set_text_frame('TCMP', ('1'))
      else:
        self.set_text_frame('TCMP', ('0'))

    if track.lyrics:
      self.tags.add(mutagen.id3.USLT(encoding=3, lang="eng", text=track.lyrics))

    if track.musicbrainz_trackid:
      self.tags.add(mutagen.id3.UFID(owner="http://musicbrainz.org", data=track.musicbrainz_trackid))

    # Convert RG tags into iTunes SoundCheck
    if track.replaygain_track_gain:
      self.set_replaygain("track", track.replaygain_track_gain, track.replaygain_track_peak)

    # Setting 2nd will force the iTunNORM comment to be Album gain.
    if track.replaygain_album_gain:
      self.set_replaygain("album", track.replaygain_album_gain, track.replaygain_album_peak)

    if track.discnumber and track.disctotal:
      self.set_text_frame('TPOS', "%d/%d" % (track.discnumber, track.disctotal))

    # Artwork time..
    if track.cover_file and os.path.exists(track.cover_file):

      if track.cover_file.endswith(".jpg"):
        mime = "image/jpeg"
      else:
        mime = "image/png"

      self.tags.delall("APIC")

      with open(track.cover_file, 'rb') as fh:
        self.tags.add(mutagen.id3.APIC(encoding=0, mime=mime, type=3, desc='', data=fh.read()))

    self.set_txxx_frame('FLAC_CHECKSUM', track.checksum)
    self.set_txxx_frame('FLAC_MTIME', track.mtime)

    self.tags.save(filename)
