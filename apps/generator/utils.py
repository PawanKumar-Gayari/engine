from apps.posts.models import SiteSettings


def is_ai_enabled():
    settings = SiteSettings.objects.first()

    if not settings:
        return False

    return settings.use_ai