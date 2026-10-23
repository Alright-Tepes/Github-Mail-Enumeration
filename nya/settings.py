import re

API = "https://api.github.com"
UA = "github-email-enum/1.0"
DELAY = 0.1
MAX_EVENTS_PAGES = 3
MAX_REPOS = 15
PAGES_REPO_MODE = 5
PAGES_SCAN_MODE = 2
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
NOREPLY_RE = re.compile(r"^(\d+)\+([^@]+)@users\.noreply\.github\.com$", re.I)
NOREPLY_DOMAIN = "users.noreply.github.com"
GMAIL_DOMAINS = {"gmail.com", "googlemail.com"}
USERNAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}$")
RATE = {"limit": None, "remaining": None, "reset": None}
