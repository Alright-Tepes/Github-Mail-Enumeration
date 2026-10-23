from .settings import API
from .settings import UA
from .hdict import hdict
from .record_rate import record_rate
import json
import time
import urllib.error
import urllib.parse
import urllib.request

def gh_get(path_or_url, token=None, **params):
    url = path_or_url if path_or_url.startswith("http") else API + path_or_url
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"Accept": "application/vnd.github+json", "User-Agent": UA}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)

    last_err = ""
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                code = resp.getcode()
                hd = hdict(resp.headers)
                record_rate(hd)
                return code, hd, resp.read()
        except urllib.error.HTTPError as e:
            code = e.code
            hd = hdict(e.headers or {})
            record_rate(hd)
            body = e.read() or b""
            if code == 403:
                retry_after = hd.get("retry-after")
                if hd.get("x-ratelimit-remaining") == "0" or retry_after:
                    return code, hd, body
                time.sleep(1.2 * (attempt + 1))
                continue
            if code in (500, 502, 503, 504):
                time.sleep(1.2 * (attempt + 1))
                continue
            return code, hd, body
        except (urllib.error.URLError, OSError) as e:
            last_err = str(e)
            time.sleep(1.2 * (attempt + 1))
    return -1, {}, json.dumps({"message": "network error: " + last_err}).encode("utf-8")
