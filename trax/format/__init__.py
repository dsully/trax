""" Abstraction for audio file formats. """

import logging

from trax.format.flac import FLAC
from trax.format.mp3  import MP3
from trax.format.mp4  import MP4

log = logging.getLogger(__name__)

FORMAT_MAP = {
  'flac': FLAC,
  'mp3' : MP3,
  'mp4' : MP4,
  'm4a' : MP4,
}

EXTENSION_MAP = {
  'flac': 'flac',
  'alac': 'm4a',
  'aac' : 'm4a',
  'mp3' : 'mp3',
  'ogg' : 'ogg',
}

def load(track, filetype=None):
  """ Load a Format class for a given track. """

  if filetype is None:
    filetype = track.filetype

  if filetype in FORMAT_MAP:
    return FORMAT_MAP[filetype](track)

def extension_for_codec(extension):
  return EXTENSION_MAP.get(extension, None)
