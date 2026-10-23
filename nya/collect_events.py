from .settings import DELAY
from .settings import MAX_EVENTS_PAGES
from .gh_get import gh_get
from .http_label import http_label
from .parse_json import parse_json
from .console import Fore
import time

def collect_events(store, token, username):
    total, push_count = 0, 0
    for page in range(1, MAX_EVENTS_PAGES + 1):
        status, hd, body = gh_get("/users/%s/events/public" % username, token,
                                  per_page=100, page=page)
        if status != 200:
            print(Fore.RED + "[!] events: %s" % http_label(status))
            break
        events = parse_json(body, [])
        if not events:
            break
        total += len(events)
        for ev in events:
            if ev.get("type") != "PushEvent":
                continue
            push_count += 1
            repo_name = (ev.get("repo") or {}).get("name") or "?"
            for c in (ev.get("payload") or {}).get("commits", []):
                a = c.get("author") or {}
                store.add(a.get("email"), name=a.get("name"),
                          source="events:%s" % repo_name, is_target=True)
        if len(events) < 100:
            break
        time.sleep(DELAY)
    print(Fore.GREEN + "[*] events: %d olay tarandi (%d push)" % (total, push_count))
