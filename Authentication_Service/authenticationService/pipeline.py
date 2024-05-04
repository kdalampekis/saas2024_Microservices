def prevent_duplicate_association(strategy, details, backend, user=None, *args, **kwargs):
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, kwargs['response']['sub'])
    if social:
        if user and social.user != user:
            return {'user': social.user}
    return {}
