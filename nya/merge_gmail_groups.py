from .etype import etype
from .gmail_canonical import gmail_canonical

def merge_gmail_groups(store):
    groups = {}
    for email, ent in store.emails():
        if etype(email) != "gmail":
            continue
        canon = gmail_canonical(email)
        g = groups.setdefault(canon, {
            "count": 0, "names": set(), "logins": set(),
            "sources": set(), "target_hits": 0, "variants": set(),
        })
        g["count"] += ent["count"]
        g["names"] |= ent["names"]
        g["logins"] |= ent["logins"]
        g["sources"] |= ent["sources"]
        g["target_hits"] += ent["target_hits"]
        g["variants"].add(email)
    return groups
