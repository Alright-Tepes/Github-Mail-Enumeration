from .settings import DELAY
from .settings import MAX_REPOS
from .settings import PAGES_SCAN_MODE
from .collect_commits import collect_commits
from .gh_get import gh_get
from .http_label import http_label
from .parse_json import parse_json
from .console import Fore
import time

def collect_user_repos(store, token, username, target_login):
    status, hd, body = gh_get("/users/%s/repos" % username, token,
                              per_page=100, sort="pushed", page=1)
    if status != 200:
        print(Fore.RED + "[!] repo listesi: %s" % http_label(status))
        return
    repos = parse_json(body, [])
    own = [r for r in repos if not r.get("fork")]
    forks = [r for r in repos if r.get("fork")]
    picked = (own + forks)[:MAX_REPOS]
    print(Fore.CYAN + "[*] %d repo taranacak (en son pushlananlar; fork'lar sona alindi)" % len(picked))
    for i, repo in enumerate(picked, 1):
        full = repo.get("full_name")
        if not full:
            continue
        print(Fore.BLUE + "    [%d/%d] %s" % (i, len(picked), full))
        collect_commits(store, token, full, pages=PAGES_SCAN_MODE,
                        target_login=target_login, source="repo:%s" % full)
        time.sleep(DELAY)
