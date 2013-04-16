#!/usr/bin/python

import setuptools

# Don't install deps for development mode.
setuptools.bootstrap_install_from = None

setuptools.setup(
  name = 'trax',
  version = '0.1',
  license = 'BSD',
  description = 'Music DB & Transcoding Utilities',
  author = 'Dan Sully',
  author_email = 'daniel-python@electricrain.com',
  url = 'https://github.com/dsully/trax',
  platforms = 'any',

  packages = ['trax'],

  scripts = [
    'bin/find-albumartist',
    'bin/find-empty-genre',
    'bin/find-missing-puid',
    'bin/fix-various-artists-compilations',
    'bin/flac-add-padding',
    'bin/flac-add-replaygain',
    'bin/trax-import',
    'bin/trax-transcode',
  ],

  zip_safe = False,
  verbose = False,
)
