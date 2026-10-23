from .gh_get import gh_get
from .http_label import http_label
from .parse_json import parse_json

def fetch_profile(token, username):
    status, hd, body = gh_get("/users/%s" % username, token)
    data = parse_json(body, {})
    if status == 404:
        return None, "Kullanici bulunamadi (404)."
    if status == 403:
        return None, "GitHub API limiti doldu (403). Token kullanin veya bir saat sonra deneyin."
    if status != 200:
        return None, "Profil alinamadi (%s)." % http_label(status)
    return data, None
