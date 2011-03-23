import logging

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

log = logging.getLogger('trax')
log.addHandler(handler)
log.setLevel(logging.INFO)
