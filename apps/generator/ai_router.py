from django.conf import settings


def generate_ai_content(keyword):

    provider = getattr(settings, "AI_PROVIDER", "dummy")

    try:
        if provider == "openai":
            from .ai_client import generate_ai_content
            return generate_ai_content(keyword)

        elif provider == "gemini":
            from .gemini_client import generate_gemini_content
            return generate_gemini_content(keyword)

        else:
            raise Exception("No AI provider selected")

    except Exception as e:
        print("⚠️ AI failed:", str(e))

        # 🔁 fallback to Gemini
        try:
            from .gemini_client import generate_gemini_content
            return generate_gemini_content(keyword)
        except Exception as e:
            print("❌ All AI failed:", str(e))
            raise Exception("All AI providers failed")