from .etype import etype
import csv
import re

def save_outputs(username, store, report_lines):
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", username) or "target"
    txt_path = "github_gmail_enum_%s.txt" % safe
    csv_path = "github_gmail_enum_%s.csv" % safe
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["email", "tip", "isimler", "logins", "kaynaklar", "tekrar", "hedef_hit"])
        for e, ent in sorted(store.emails()):
            w.writerow([e, etype(e),
                        "; ".join(sorted(ent["names"])),
                        "; ".join(sorted(ent["logins"])),
                        "; ".join(sorted(ent["sources"])),
                        ent["count"], ent["target_hits"]])
    return txt_path, csv_path
