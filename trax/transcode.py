"""
  Transcode one audio codec & format to another using ffmpeg.
"""

import logging
import os
import shutil
import subprocess

from qtfaststart import processor
from qtfaststart.exceptions import FastStartException

TRANSCODE_MAP = {
  'alac': 'alac',
  'aac' : 'libfaac',
  'mp3' : 'libmp3lame',
  'copy': 'copy',
}

log = logging.getLogger(__name__)

def valid_codecs():
  """ Return the list of valid codecs that can be transcoded. """

  return [k for k in TRANSCODE_MAP.keys() if k != 'copy']

def transcode(dst_file, dst_codec, src_file, src_codec=None):
  """ Transcode one audio file to another. """

  if dst_codec not in TRANSCODE_MAP:
    raise ValueError("Couldn't find the %s codec in the transcode map!")

  if src_codec and src_codec == dst_codec:
    dst_codec = 'copy'

  # ffmpeg can do the decode & encode in one shot
  command = ['ffmpeg', '-y', '-loglevel', 'quiet', '-i', src_file, '-map', '0:0', '-ac', '2', '-acodec', TRANSCODE_MAP[dst_codec], dst_file]

  path = os.path.dirname(dst_file)

  if not os.path.exists(path):
    os.makedirs(path)

  popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  popen.communicate()

  # Set the MP4 to be optimized for streaming.
  if dst_codec in ('alac', 'aac'):

    try:
      temp_file = dst_file + '.tmp'
      processor.process(dst_file, temp_file, limit=0)

      if os.path.exists(temp_file):
        shutil.move(temp_file, dst_file)
      else:
        log.error("Couldn't mark [%s] as streaming/fast start.", dst_file)

    except FastStartException:
      log.error("Couldn't mark [%s] as streaming/fast start.", dst_file)

  return popen.returncode
