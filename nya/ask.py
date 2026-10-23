import getpass
import sys

def ask(prompt, secret=False):
    if secret and sys.stdin.isatty() and sys.stdout.isatty():
        try:
            return getpass.getpass(prompt).strip()
        except Exception:
            pass
    try:
        return input(prompt).strip()
    except EOFError:
        return ""
