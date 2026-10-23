import json

def parse_json(body, default):
    try:
        return json.loads(body.decode("utf-8", "replace"))
    except Exception:
        return default
