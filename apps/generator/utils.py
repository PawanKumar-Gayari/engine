import os
from apps.posts.models import SiteSettings


def is_ai_enabled():
    """
    Decide whether AI should be used or not.

    Priority:
    1. Database (SiteSettings)
    2. .env fallback
    """

    settings = SiteSettings.objects.first()

    # 🔍 Debug logs (important)
    print("\n===== AI ENABLE CHECK =====")
    print("DB SETTINGS OBJECT:", settings)

    # ✅ If DB exists → use DB value
    if settings:
        print("DB AI VALUE:", settings.use_ai)
        return settings.use_ai

    # 🔁 Fallback to .env
    env_val = os.getenv("USE_AI", "False") == "True"
    print("ENV AI VALUE:", env_val)

    return env_val