def collect_profile(store, token, profile, target_login):
    email = profile.get("email")
    if email:
        store.add(email, name=profile.get("name") or profile.get("login"),
                  login=profile.get("login"), source="profil", is_target=True)
