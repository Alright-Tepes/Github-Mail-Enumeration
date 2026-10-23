from .settings import GMAIL_DOMAINS
from .settings import NOREPLY_DOMAIN

def etype(email):
    domain = email.rsplit("@", 1)[-1]
    if domain in GMAIL_DOMAINS:
        return "gmail"
    if domain == NOREPLY_DOMAIN:
        return "noreply"
    return "other"
