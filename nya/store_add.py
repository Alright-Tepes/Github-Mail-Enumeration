from .settings import EMAIL_RE

def store_add(self, email, name=None, login=None, source=None, is_target=False):
        if not email:
            return
        email = email.strip()
        if not EMAIL_RE.match(email):
            return
        e = email.lower()
        ent = self.by_email.setdefault(e, {
            "count": 0, "names": set(), "logins": set(),
            "sources": set(), "target_hits": 0,
        })
        ent["count"] += 1
        if name and name.strip():
            ent["names"].add(name.strip())
        if login and login.strip():
            ent["logins"].add(login.strip())
        if source:
            ent["sources"].add(source)
        if is_target:
            ent["target_hits"] += 1
