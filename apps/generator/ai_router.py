from django.conf import settings


def generate_ai_content(keyword: str, intent: str = "general") -> str:
    """
    🔥 Smart AI Router (Advanced + Intent Aware)

    Priority:
    1. OpenRouter (Primary)
    2. Gemini (Fallback)
    3. OpenAI (Last fallback)
    """

    provider = getattr(settings, "AI_PROVIDER", None)

    print("\n===== AI ROUTER DEBUG =====")
    print("🔥 ACTIVE PROVIDER:", provider)
    print("KEYWORD:", keyword)
    print("🧠 INTENT:", intent)

    # 🔥 Default fallback provider
    if not provider:
        print("⚠️ No provider set → defaulting to openrouter")
        provider = "openrouter"

    # =========================
    # 🥇 PRIMARY CALL
    # =========================
    try:
        if provider == "openrouter":
            print("🚀 Using OpenRouter...")

            from .openrouter_client import generate_openrouter_content

            return generate_openrouter_content(keyword, intent)

        elif provider == "gemini":
            print("🚀 Using Gemini...")

            from .gemini_client import generate_gemini_content

            return generate_gemini_content(keyword)

        elif provider == "openai":
            print("🚀 Using OpenAI...")

            from .ai_client import generate_ai_content as openai_generate

            return openai_generate(keyword)

        else:
            raise Exception(f"Invalid AI_PROVIDER: {provider}")

    except Exception as primary_error:
        print("⚠️ PRIMARY FAILED:", str(primary_error))

    # =========================
    # 🔁 FALLBACK 1: OPENROUTER
    # =========================
    try:
        print("🔁 Fallback → OpenRouter...")

        from .openrouter_client import generate_openrouter_content

        return generate_openrouter_content(keyword, intent)

    except Exception as e:
        print("⚠️ OpenRouter fallback failed:", str(e))

    # =========================
    # 🔁 FALLBACK 2: GEMINI
    # =========================
    try:
        print("🔁 Fallback → Gemini...")

        from .gemini_client import generate_gemini_content

        return generate_gemini_content(keyword)

    except Exception as e:
        print("⚠️ Gemini fallback failed:", str(e))

    # =========================
    # 🔁 FALLBACK 3: OPENAI
    # =========================
    try:
        print("🔁 Fallback → OpenAI...")

        from .ai_client import generate_ai_content as openai_generate

        return openai_generate(keyword)

    except Exception as e:
        print("⚠️ OpenAI fallback failed:", str(e))

    # =========================
    # ❌ FINAL FAIL
    # =========================
    print("❌ ALL AI PROVIDERS FAILED")

    raise Exception("All AI providers failed")