import logging
import os

import mutagen

from trax.format.base import Base

log = logging.getLogger(__name__)

class FLAC(Base):
  """ FLAC Audio File. """

  # Not needed for FLAC
  txxx = {}

  def extract_artwork(self):
    """ Extract artwork metadata into a file. """

    basename = os.path.dirname(self.filename)
    tags     = mutagen.File(self.filename)

    if len(tags.pictures) == 0:
      return None

    picture = tags.pictures[0]

    if picture.mime == "image/jpeg":
      cover_file = os.path.join(basename, "cover.jpg")
    else:
      cover_file = os.path.join(basename, "cover.png")

    # Only write out if we've changed.
    if os.path.exists(cover_file):
      if self.track.mtime <= int(os.stat(cover_file).st_mtime):
        return cover_file

    try:
      with open(cover_file, "wb") as fh:
        fh.write(picture.data)

    except IOError, e:
      print "Couldn't write to file (%s): %s" % (cover_file, e)
      return None

    return cover_file
