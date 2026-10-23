import re
import urllib.error
import urllib.parse
import urllib.request

def parse_repo(text):
    text = text.strip().rstrip("/")
    if not text:
        return None
    if re.match(r"^https?://", text, re.I):
        path = urllib.parse.urlparse(text).path.strip("/")
        parts = [p for p in path.split("/") if p]
    elif "/" in text:
        parts = [p for p in text.split("/") if p]
    else:
        return None
    if len(parts) >= 2:
        owner, name = parts[0], parts[1]
        if name.endswith(".git"):
            name = name[:-4]
        return "%s/%s" % (owner, name)
    return None
