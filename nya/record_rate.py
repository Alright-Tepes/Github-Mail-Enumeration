from .settings import RATE

def record_rate(hd):
    for key, hdr in (("limit", "x-ratelimit-limit"),
                     ("remaining", "x-ratelimit-remaining"),
                     ("reset", "x-ratelimit-reset")):
        val = hd.get(hdr)
        if val is not None:
            RATE[key] = val
