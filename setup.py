#!/usr/bin/python

import setuptools

# Don't install deps for development mode.
setuptools.bootstrap_install_from = None

setuptools.setup(
  name = '',
  version = '0.1',
  license = 'BSD',
  description = open('README.txt').read(),
  author = "Dan Sully",
  author_email = "daniel-python@electricrain.com",
  url = 'https://github.com/dsully/trax',
  platforms = 'any',

  packages = 'trax',

  scripts = [
    'find-albumartist',
    'find-empty-genre',
    'find-missing-puid',
    'fix-various-artists-compilations',
    'flac-add-padding',
    'flac-add-replaygain',
    'trax-import',
    'trax-transcode',
  ],

  install_requires = [
    'mutagen',
    'sqlalchemy',
  ],

  zip_safe = False,
  #verbose = False,
)
