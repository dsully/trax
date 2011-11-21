class Base(object):

  #: Mapping of format tag to :class:`Track` attribute.
  attributes = {}

  #: User set tags to :class:`Track` attribute.
  txxx = {
    'ASIN'                             : 'asin',
    'BARCODE'                          : 'barcode',
    'CATALOGNUMBER'                    : 'catalognumber',
    'ISRC'                             : 'isrc',
    'LABEL'                            : 'label',
    'LYRICIST'                         : 'lyricist',
    'MEDIA'                            : 'media',
    'MusicBrainz Album Artist Id'      : 'musicbrainz_albumartistid',
    'MusicBrainz Album Id'             : 'musicbrainz_albumid',
    'MusicBrainz Album Status'         : 'musicbrainz_albumstatus',
    'MusicBrainz Album Type'           : 'musicbrainz_albumtype',
    'MusicBrainz Artist Id'            : 'musicbrainz_artistid',
    'MusicBrainz Disc Id'              : 'musicbrainz_discid',
    'MusicBrainz Track Id'             : 'musicbrainz_trackid',
    'MusicBrainz TRM Id'               : 'musicbrainz_trmid',
    'MusicMagic Fingerprint'           : 'musicip_fingerprint',
    'MusicIP PUID'                     : 'musicip_puid',
    'MusicBrainz Album Release Country': 'releasecountry',
    'URL_DISCOGS_RELEASE_SITE'         : 'url_discogs_release_site',
    'URL_LYRICS_SITE'                  : 'url_lyrics_site',
    'URL_WIKIPEDIA_RELEASE_SITE'       : 'url_wikipedia_release_site',
  }

  #: Tuple of genres that are gapless between tracks.
  gapless = ('Electronic', 'Trance', 'Techno', 'Ambient', 'Mashup')

  def __init__(self, track):
    self.track    = track
    self.filename = track.filename
