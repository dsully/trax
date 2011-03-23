class Base(object):

  txxx = {
    'asin':                      'ASIN',
    'barcode':                   'BARCODE',
    'catalognumber':             'CATALOGNUMBER',
    'isrc':                      'ISRC',
    'label':                     'LABEL',
    'lyricist':                  'LYRICIST',
    'media':                     'MEDIA',
    'musicbrainz_albumid':       'MusicBrainz Album Id',
    'musicbrainz_albumstatus':   'MusicBrainz Album Status',
    'musicbrainz_albumtype':     'MusicBrainz Album Type',
    'musicbrainz_albumartistid': 'MusicBrainz Album Artist Id',
    'musicbrainz_artistid':      'MusicBrainz Artist Id',
    'musicbrainz_discid':        'MusicBrainz Disc Id',
    'musicbrainz_trmid':         'MusicBrainz TRM Id',
    'musicbrainz_trackid':       'MusicBrainz Track Id',
    'musicip_fingerprint':       'MusicMagic Fingerprint',
    'musicip_puid':              'MusicIP PUID',
    'releasecountry':            'MusicBrainz Album Release Country',
    'url_discogs_release_site':  'URL_DISCOGS_RELEASE_SITE',
    'url_lyrics_site':           'URL_LYRICS_SITE',
    'url_wikipedia_release_site':'URL_WIKIPEDIA_RELEASE_SITE',
  }

  gapless = {
    "Electronic": True,
    "Trance":     True,
    "Techno":     True,
    "Ambient":    True,
    "Mashup":     True,
  }

  def __init__(self, track):
    self.track    = track
    self.filename = track.filename

  def apply_replaygain(self):
    pass
