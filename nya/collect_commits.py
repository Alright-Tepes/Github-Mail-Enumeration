from .settings import DELAY
from .gh_get import gh_get
from .http_label import http_label
from .parse_json import parse_json
from .console import Fore
import time

def collect_commits(store, token, full_name, pages, target_login=None, source=None):
    source = source or ("repo:" + full_name)
    for page in range(1, pages + 1):
        status, hd, body = gh_get("/repos/%s/commits" % full_name, token,
                                  per_page=100, page=page)
        if status == 409:
            break
        if status != 200:
            print(Fore.RED + "      [!] commit: %s" % http_label(status))
            break
        commits = parse_json(body, [])
        if not commits:
            break
        for c in commits:
            commit = c.get("commit") or {}
            ca = commit.get("author") or {}
            cc = commit.get("committer") or {}
            a_login = ((c.get("author") or {}).get("login") or "").lower()
            c_login = ((c.get("committer") or {}).get("login") or "").lower()
            is_target = target_login and (a_login == target_login or c_login == target_login)
            store.add(ca.get("email"), name=ca.get("name"),
                      login=(c.get("author") or {}).get("login"),
                      source=source, is_target=bool(is_target))
            store.add(cc.get("email"), name=cc.get("name"),
                      login=(c.get("committer") or {}).get("login"),
                      source=source, is_target=bool(is_target))
        if len(commits) < 100:
            break
        time.sleep(DELAY)
