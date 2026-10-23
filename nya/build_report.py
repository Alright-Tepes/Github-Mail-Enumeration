from .settings import NOREPLY_RE
from .etype import etype

def build_report(username, store, gmail_groups):
    emails = dict(store.emails())
    noreply = sorted(e for e in emails if etype(e) == "noreply")
    others = sorted(e for e in emails if etype(e) == "other")

    L = []
    L.append("")
    L.append("=" * 64)
    L.append(" RAPOR - hedef: %s" % username)
    L.append("=" * 64)
    L.append(" Benzersiz e-posta: %d | Gmail (normalize): %d | "
             "Noreply: %d | Diger: %d" % (len(emails), len(gmail_groups),
                                          len(noreply), len(others)))

    L.append("")
    L.append("[1] GMAIL")
    if gmail_groups:
        for canon, g in sorted(gmail_groups.items(), key=lambda kv: (-kv[1]["count"], kv[0])):
            tag = "  [hedef]" if g["target_hits"] else ""
            L.append("  %s%s   (toplam tekrar: %d)" % (canon, tag, g["count"]))
            if g["names"]:
                L.append("      isim  : %s" % ", ".join(sorted(g["names"])))
            if g["logins"]:
                L.append("      login : %s" % ", ".join(sorted(g["logins"])))
            variants = sorted(g["variants"] - {canon})
            if variants:
                L.append("      varyant: %s" % ", ".join(variants))
            if g["sources"]:
                L.append("      kaynak: %s" % ", ".join(sorted(g["sources"])))
    else:
        L.append("  - (yok)")
        L.append("  [i] Gmail bulunamadi. Olasi nedenler:")
        L.append("      * Kullanici 'Keep my email addresses private' ayarini acmis olabilir")
        L.append("        -> commit'lerde yalnizca noreply adresi gorunur (asagiya bakin)")
        L.append("      * Eski commit'ler diger dallarda/katkidiginiz repo'larda olabilir")
        L.append("      * Daha derin tarama icin token girin ve/veya repo linki belirterek deneyin")

    L.append("")
    L.append("[2] GITHUB NOREPLY")
    if noreply:
        for e in noreply:
            ent = emails[e]
            tag = "  [hedef]" if ent["target_hits"] else ""
            L.append("  %s%s   (tekrar: %d)" % (e, tag, ent["count"]))
            m = NOREPLY_RE.match(e)
            if m:
                L.append("      GitHub ID: %s | noreply adi: %s" % (m.group(1), m.group(2)))
            if ent["names"]:
                L.append("      isim  : %s" % ", ".join(sorted(ent["names"])))
            if ent["sources"]:
                L.append("      kaynak: %s" % ", ".join(sorted(ent["sources"])))
    else:
        L.append("  - (yok)")

    L.append("")
    L.append("[3] DIGER E-POSTALAR")
    if others:
        for e in others[:20]:
            ent = emails[e]
            tag = "  [hedef]" if ent["target_hits"] else ""
            L.append("  %s%s   (tekrar: %d)" % (e, tag, ent["count"]))
            if ent["names"]:
                L.append("      isim  : %s" % ", ".join(sorted(ent["names"])))
            if ent["logins"]:
                L.append("      login : %s" % ", ".join(sorted(ent["logins"])))
        if len(others) > 20:
            L.append("  ... ve %d tane daha (CSV dosyasina bakin)" % (len(others) - 20))
    else:
        L.append("  - (yok)")

    L.append("")
    L.append("[i] Notlar:")
    L.append("    - [hedef] = GitHub login'i hedef kullaniciyla eslesen veya hedefin")
    L.append("      kendi event akisindan gelen e-postalar")
    L.append("    - noreply adresi gercek e-posta degildir; GitHub ID korelasyon icindir")
    return L
