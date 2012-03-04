Trax: Simple audio database & transcoding tools.
================================================

Installation
------------

Use Python's *pip* installer. Install [pip](http://www.pip-installer.org/en/latest/installing.html) if you don't have it.

Install trax using pip:

    pip install https://github.com/dsully/trax/zipball/master

Required External Dependencies
------------------------------

* ffmpeg

* mp4file (from the [mp4v2](http://code.google.com/p/mp4v2/) toolset).

Optional External Dependencies
------------------------------

To use the *flac-add-padding* tool, you need [pyflac](https://github.com/dsully/pyflac/zipball/master), which requires the *SWIG* & *FLAC* development libraries.

Usage
-----

To import files into the database, run:

    trax-import --progress --path /path/to/your/music

Currently supported input formats are: FLAC, MP4 (ALAC/AAC) & MP3.

Once your metadata is imported, you may optionally run:

* flac-add-padding
* flac-add-replaygain
* fix-various-artists-compilations

To transcode audio & copy tag data, run:

    trax-transcode --progress --source-dir /path/to/your/music --dest-dir /path/to/your/transcoded {aac,alac,mp3}
