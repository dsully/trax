""" Abstraction for audio file formats. """

import logging
import os

from trax.format.flac import FLAC
from trax.format.mp3  import MP3
from trax.format.mp4  import MP4

log = logging.getLogger(__name__)

format_map = {
  'flac': FLAC,
  'mp3' : MP3,
  'mp4' : MP4,
  'm4a' : MP4,
}

def load(track):

  if track.filetype in format_map:
    return format_map[track.filetype](track)
