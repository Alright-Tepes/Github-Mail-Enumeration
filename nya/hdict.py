def hdict(headers):
    try:
        return {k.lower(): v for k, v in headers.items()}
    except Exception:
        return {}
