def gmail_canonical(email):
    local, domain = email.rsplit("@", 1)
    if domain == "googlemail.com":
        domain = "gmail.com"
    base = local.split("+")[0].replace(".", "")
    return base + "@" + domain
