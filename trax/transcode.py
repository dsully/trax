"""
  Transcode one audio codec & format to another using ffmpeg.
"""

import os
import subprocess

TRANSCODE_MAP = {
  'alac': 'alac',
  'aac' : 'libfaac',
  'mp3' : 'libmp3lame',
  'copy': 'copy',
}

def valid_codecs():
  """ Return the list of valid codecs that can be transcoded. """

  return [k for k in TRANSCODE_MAP.iterkeys() if k != 'copy']

def transcode(dst_file, dst_codec, src_file, src_codec=None):
  """ Transcode one audio file to another. """

  if dst_codec not in TRANSCODE_MAP:
    raise ValueError("Couldn't find the %s codec in the transcode map!")

  if src_codec and src_codec == dst_codec:
    dst_codec = 'copy'

  # ffmpeg can do the decode & encode in one shot
  command = ['ffmpeg', '-y', '-loglevel', 'quiet', '-i', src_file, '-ac', '2', '-acodec', TRANSCODE_MAP[dst_codec], dst_file]

  path = os.path.dirname(dst_file)

  if not os.path.exists(path):
    os.makedirs(path)

  popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  popen.communicate()

  # Set the MP4 to be optimized for streaming.
  if dst_codec in ('alac', 'aac'):
    subprocess.call(['mp4file', '--optimize', '-q', dst_file])

  return popen.returncode
