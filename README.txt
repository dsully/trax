Trax: A simple audio database & tools.
--------------------------------------

To import files into the database, run:

* Run: trax-import
  - This also extracts cover art.

Currently supported file formats are: FLAC, MP4 (ALAC/AAC) & MP3. 

Once your metadata is imported, you may optionally run:

* flac-add-padding
* flac-add-replaygain
* fix-various-artists-compilations

Then to transcode & convert tags, run:

* trax-transcode

=====================
Required Dependencies
=====================

* ffmpeg

* mp4file (from the mp4v2 toolset).

=====================
Optional Dependencies
=====================

* 'pyflac' from: https://github.com/dsully/pyflac/zipball/master

  - requires SWIG & FLAC headers & development libraries.
