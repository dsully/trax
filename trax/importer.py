"""
  Parse audio metadata & import it into the database.
"""

import logging
import os

import mutagen

from trax.format import load as load_format
from trax.format import FORMAT_MAP
from trax.schema import Track

log = logging.getLogger(__name__)

def import_track(filename, last_updated, force=False):
  """ Import a Track into the database. """

  filetype = os.path.splitext(filename.lower())[1].replace('.', '')

  if filetype not in FORMAT_MAP:
    return None

  mtime = int(os.stat(filename).st_mtime)

  # Empty database (or incomplete import).
  if last_updated.value == 0:

    track = Track(filename=filename)

  else:

    # Otherwise, try and find the track to update it's metadata.
    try:
      track = Track.query.filter(Track.filename==filename).one()
    except:
      track = Track(filename=filename)

    # Skip if we're already up to date.
    if not force and track.mtime and track.mtime == mtime:
      return None

    # The track hasn't been updated since our last run.
    if not force and track.id and mtime <= last_updated.value:
      return None

  tags = mutagen.File(filename)

  if tags is None:
    log.warn("Couldn't parse any tags for: %s", filename)
    return None

  log.debug('Processing "%s"', filename)

  track.mtime    = mtime
  track.filetype = filetype
  container      = load_format(track)

  # FLAC will have a MD5 built in. Generate for other formats.
  try:
    track.checksum = str(tags.info.md5_signature)
  except AttributeError:
    try:
      track.checksum = container.md5_signature
    except AttributeError:
      log.debug("%s didn't have a md5_signature & one couldn't be generated!", filename)

  # Map metadata values to the Track object.
  for tag in tags.iterkeys():

    attribute = container.attributes.get(tag, tag)

    # Look for TXXX as well, when importing non-Vorbis tags.
    if tag.startswith('TXXX:'):
      attribute = container.txxx.get(tag.replace('TXXX:', ''), None)

    try:
      if attribute and hasattr(track, attribute.lower()):
        value = tags[tag][0]

        # ID3 timestamps need conversion to strings.
        if value.__class__.__name__ == 'ID3TimeStamp':
          value = unicode(value)

        setattr(track, attribute.lower(), value)

    except UnicodeEncodeError as e:
      log.warn("Couldn't set attribute on %s: [%s]", filename, e)

  track.compilation = False

  if 'compilation' in tags:
    if tags["compilation"][0] == "true" or tags["compilation"][0] == u'1':
      track.compilation = True

  if 'fingerprint' in tags:
    track.musicip_fingerprint = tags['fingerprint'][0]

  # Handle both Album & Track replaygain.
  for rgtype in ['album', 'track']:

    gain = 'replaygain_%s_gain' % rgtype
    peak = 'replaygain_%s_peak' % rgtype

    if gain in tags:
      setattr(track, gain, tags[gain][0])
      setattr(track, peak, tags[peak][0])

  # Artwork time..
  try:
    track.cover_file = container.extract_artwork()
  except AttributeError:
    pass

  return track
