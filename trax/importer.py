"""
  Parse audio metadata & import it into the database.
"""

import logging
import os
import re

import mutagen

import trax.format
from trax.schema import Track

log = logging.getLogger(__name__)

filetypes = ['flac', 'mp3', 'm4a', 'mp4']

def import_track(filename, last_updated, force=False):
  """ Import a Track into the database. """

  filetype = os.path.splitext(filename.lower())[1].replace('.', '')

  if filetype not in filetypes:
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
  track.checksum = str(tags.info.md5_signature)

  # Map metadata values to the Track object.
  for attribute in tags.iterkeys():
    if hasattr(track, attribute.lower()):
      setattr(track, attribute.lower(), tags[attribute][0])

  if 'compilation' in tags:
    if tags["compilation"][0] == "true" or tags["compilation"][0] == u'1':
      track.compilation = True
    else:
      track.compilation = False

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
    track.cover_file = trax.format.load(track).extract_artwork()
  except AttributeError:
    pass

  return track
