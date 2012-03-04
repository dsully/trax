import logging
import os

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

log = logging.getLogger('trax')
log.addHandler(handler)
log.setLevel(logging.INFO)

def which(filename):
  """ Find an executable's path. """

  for entry in os.environ.get('PATH', os.defpath).split(os.pathsep):
    path = os.path.join(entry, filename)

    if os.access(path, os.F_OK|os.X_OK):
      return path

  return None
