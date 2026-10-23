import sys

from os import system

from nya.console import Fore
from nya.settings import PAGES_REPO_MODE, RATE, USERNAME_RE
from nya.store import Store
from nya.ask import ask
from nya.build_report import build_report
from nya.collect_commits import collect_commits
from nya.collect_events import collect_events
from nya.collect_profile import collect_profile
from nya.collect_user_repos import collect_user_repos
from nya.fetch_profile import fetch_profile
from nya.merge_gmail_groups import merge_gmail_groups
from nya.out_utf8 import out_utf8
from nya.parse_repo import parse_repo
from nya.save_outputs import save_outputs

system("cls")


def main():
    out_utf8()
    args = sys.argv[1:]
    print(Fore.CYAN + "=" * 64)
    print(Fore.CYAN + " GitHub Gmail Enumeration")
    print(Fore.CYAN + "=" * 64)

    if args:
        username = args[0].strip().lstrip("@")
        repo_raw = args[1].strip() if len(args) > 1 else ""
        token = args[2].strip() if len(args) > 2 else ""
    else:
        username = ask("[?] GitHub kullanici adi: ").strip().lstrip("@")
        repo_raw = ask("[?] Repo linki (opsiyonel, bos gecilebilir): ").strip()
        token = ask("[?] GitHub token (opsiyonel, bos gecilebilir): ", secret=True).strip()

    if not USERNAME_RE.match(username):
        print(Fore.RED + "[!] Gecersiz GitHub kullanici adi.")
        return 1

    repo_full = parse_repo(repo_raw) if repo_raw else None
    if repo_raw and not repo_full:
        print(Fore.RED + "[!] Repo linki anlasilamadi. Ornek: https://github.com/owner/repo")
        return 1

    token = token or None
    profile, err = fetch_profile(token, username)
    if err:
        print(Fore.RED + "[!] " + err)
        return 1

    target_login = (profile.get("login") or username).lower()
    print(Fore.CYAN + "[*] Hedef: %s | Isim: %s | Public repo: %s"
          % (profile.get("login") or username,
             profile.get("name") or "-",
             profile.get("public_repos", "?")))

    store = Store()
    collect_profile(store, token, profile, target_login)

    if repo_full:
        print(Fore.BLUE + "[*] Repo taramasi: %s (%d sayfaya kadar)"
              % (repo_full, PAGES_REPO_MODE))
        collect_commits(store, token, repo_full, pages=PAGES_REPO_MODE,
                        target_login=target_login)
    else:
        collect_events(store, token, username)
        collect_user_repos(store, token, username, target_login)

    gmail_groups = merge_gmail_groups(store)
    report_lines = build_report(username, store, gmail_groups)
    for line in report_lines:
        if line.startswith((" RAPOR", "[1]", "[2]", "[3]", "[i]")) or line.startswith("="):
            color = Fore.CYAN
        elif "@" in line:
            color = Fore.GREEN
        else:
            color = Fore.WHITE
        print(color + line)

    txt_path, csv_path = save_outputs(username, store, report_lines)
    print("")
    print(Fore.GREEN + "[*] Rapor kaydedildi: %s" % txt_path)
    print(Fore.GREEN + "[*] CSV kaydedildi : %s" % csv_path)

    if RATE["remaining"] is not None:
        print(Fore.YELLOW + "[i] API limiti: %s/%s istek kaldi" % (RATE["remaining"], RATE["limit"] or "?"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Iptal edildi.")
        sys.exit(130)
