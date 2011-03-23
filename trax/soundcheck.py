# Array for SoundCheck data. These values aren't used by iTunes, so they can be static.
sc_defaults = [0, 0, 0, 0, "00024CA8", "00024CA8", "00007FFF", "00007FFF", "00024CA8", "00024CA8"]

def replay_gain_to_soundcheck(gain, peak):
  """ Convert replay gain values into iTunes sound check. """

  gain = float(gain.replace(' dB', ''))
  peak = float(peak)

  def _gain2sc(gain, base):
    result = round((10 ** (-gain / 10)) * base)

    if (result > 65534):
      result = 65534

    return "%08X" % result

  soundcheck = sc_defaults
  soundcheck[0] = _gain2sc(gain, 1000)
  soundcheck[2] = _gain2sc(gain, 2500)
  soundcheck[1] = soundcheck[0]
  soundcheck[3] = soundcheck[2]

  return " %s" % ' '.join(soundcheck)
