from django.conf import settings
from django.core.cache import cache

import time
import logging
import random
import hashlib

from apps.generator.model_router import ModelRouter

logger = logging.getLogger(__name__)

# =========================
# ⚙️ CONFIG
# =========================
MAX_RETRIES = 3
MIN_CONTENT_LENGTH = 400
BASE_DELAY = 1
CACHE_TTL = 60 * 30
REQUEST_TIMEOUT = 20


# =========================
# 🚀 MAIN ENTRY
# =========================
def generate_ai_content(
    keyword: str,
    intent: str = "general",
    stage: str = "draft",
    base_content: str = ""
):

    keyword = (keyword or "").strip()

    if not keyword:
        raise Exception("Empty keyword")

    cache_key = _build_cache_key(keyword, intent, stage)

    # =========================
    # ⚡ CACHE
    # =========================
    cached = cache.get(cache_key)
    if cached:
        logger.info(f"[CACHE HIT] {stage}")
        return cached

    router = ModelRouter()
    model_info = router.get_model(stage)

    provider = model_info["provider"]
    model = model_info["model"]

    logger.info(f"[ROUTER] Stage={stage} → {provider}:{model}")

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            start_time = time.time()

            content = _call_with_timeout(
                provider,
                keyword,
                intent,
                stage,
                base_content,
                model
            )

            duration = round(time.time() - start_time, 2)

            if _is_valid_content(content):

                score = _score_content(content, keyword)

                logger.info(
                    f"[SUCCESS] {provider} | {stage} | {duration}s | Score={score}"
                )

                cache.set(cache_key, content, CACHE_TTL)

                return content.strip()

            raise Exception("Low quality content")

        except Exception as e:
            last_error = e

            logger.warning(f"[FAIL] {provider} | Attempt {attempt} | {e}")

            delay = BASE_DELAY * (2 ** (attempt - 1))
            delay += random.uniform(0, 0.5)

            time.sleep(delay)

    logger.error("[AI ROUTER] All retries failed")

    raise Exception(f"AI failed: {last_error}")


# =========================
# 🔑 CACHE KEY
# =========================
def _build_cache_key(keyword, intent, stage):
    raw = f"{keyword}:{intent}:{stage}"
    return "ai:" + hashlib.md5(raw.encode()).hexdigest()


# =========================
# ⏱️ TIMEOUT
# =========================
def _call_with_timeout(provider, keyword, intent, stage, base_content, model):

    start = time.time()

    content = _call_provider(
        provider,
        keyword,
        intent,
        stage,
        base_content,
        model
    )

    if (time.time() - start) > REQUEST_TIMEOUT:
        raise Exception("Timeout")

    return content


# =========================
# 🔌 PROVIDER CALL
# =========================
def _call_provider(provider, keyword, intent, stage, base_content, model):

    if provider == "openrouter":
        from .openrouter_client import generate_openrouter_content
        return generate_openrouter_content(
            keyword,
            intent=intent,
            stage=stage,
            base_content=base_content,
            model=model
        )

    elif provider == "gemini":
        from .gemini_client import generate_gemini_content
        return generate_gemini_content(
            keyword,
            stage=stage,
            base_content=base_content
        )

    elif provider == "openai":
        from .ai_client import generate_ai_content as openai_generate
        return openai_generate(
            keyword,
            stage=stage,
            base_content=base_content
        )

    raise Exception(f"Unsupported provider: {provider}")


# =========================
# ✅ VALIDATION
# =========================
def _is_valid_content(content):

    if not content:
        return False

    if len(content) < MIN_CONTENT_LENGTH:
        return False

    text = content.lower()

    if any(x in text for x in ["lorem", "dummy", "error"]):
        return False

    if text.count(".") < 5:
        return False

    return True


# =========================
# 📊 SCORING
# =========================
def _score_content(content, keyword):

    text = content.lower()
    words = text.split()

    score = 0

    if len(words) > 1000:
        score += 30
    elif len(words) > 700:
        score += 20

    keyword_count = text.count(keyword.lower())

    if keyword_count > 5:
        score += 20

    density = (keyword_count / len(words)) * 100 if words else 0

    if 1 <= density <= 3:
        score += 20

    if "introduction" in text:
        score += 10

    if "conclusion" in text:
        score += 10

    return score