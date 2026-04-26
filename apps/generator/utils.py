import os
import time
import random
import logging
import threading
from django.core.cache import cache
from django.db import DatabaseError
from apps.posts.models import SiteSettings

# =========================
# ⚙️ CONFIG
# =========================
CACHE_KEY = "ai_enabled_status"
LOCK_KEY = "ai_enabled_lock"

CACHE_TTL = 60
LOCK_TTL = 5

LOCAL_TTL = 10
NEGATIVE_CACHE_TTL = 30  # DB fail case

# 🔒 thread-safe local cache
LOCAL_FALLBACK = {"value": None, "ts": 0}
LOCAL_LOCK = threading.Lock()

logger = logging.getLogger(__name__)


def is_ai_enabled() -> bool:
    """
    🚀 Enterprise Feature Flag System (AI Toggle)

    Layers:
    1. ENV override (force control)
    2. Local memory cache
    3. Distributed cache
    4. DB
    5. ENV fallback

    Features:
    - Multi-layer caching
    - Negative caching
    - Stale-while-revalidate
    - Stampede protection
    - Thread safety
    """

    now = time.time()

    # =========================
    # 🔥 ENV OVERRIDE (FORCE)
    # =========================
    force = os.getenv("FORCE_AI")
    if force is not None:
        val = _parse_bool(force)
        logger.warning(f"[AI CHECK] FORCE override → {val}")
        return val

    # =========================
    # ⚡ LOCAL CACHE
    # =========================
    with LOCAL_LOCK:
        if LOCAL_FALLBACK["value"] is not None:
            if now - LOCAL_FALLBACK["ts"] < LOCAL_TTL:
                logger.debug("[AI CHECK] Local hit")
                return LOCAL_FALLBACK["value"]

    # =========================
    # ⚡ REDIS CACHE
    # =========================
    cached = cache.get(CACHE_KEY)
    if cached is not None:
        logger.debug(f"[AI CHECK] Cache hit → {cached}")
        _update_local_cache(cached)
        return cached

    logger.debug("[AI CHECK] Cache miss")

    # =========================
    # 🔒 LOCK
    # =========================
    if cache.add(LOCK_KEY, True, LOCK_TTL):
        try:
            value = _get_from_db_safe()

            ttl = CACHE_TTL + random.randint(5, 15)
            cache.set(CACHE_KEY, value, ttl)

            _update_local_cache(value)
            return value

        finally:
            cache.delete(LOCK_KEY)

    # =========================
    # ⏳ WAIT (STALE-WHILE-REVALIDATE)
    # =========================
    for _ in range(5):
        time.sleep(0.1)
        cached = cache.get(CACHE_KEY)
        if cached is not None:
            _update_local_cache(cached)
            return cached

    # =========================
    # 🚨 FINAL FALLBACK
    # =========================
    logger.warning("[AI CHECK] Lock timeout → fallback ENV")

    value = _get_from_env()
    _update_local_cache(value)
    return value


# =========================
# 🗄️ SAFE DB FETCH
# =========================
def _get_from_db_safe() -> bool:
    try:
        settings_obj = (
            SiteSettings.objects
            .only("use_ai")
            .first()
        )

        if settings_obj:
            value = bool(settings_obj.use_ai)
            logger.debug(f"[AI CHECK] DB → {value}")
            return value

    except DatabaseError as e:
        logger.error(f"[AI CHECK] DB error → {str(e)}")

        # 🔥 NEGATIVE CACHE (prevent spam)
        fallback = _get_from_env()
        cache.set(CACHE_KEY, fallback, NEGATIVE_CACHE_TTL)
        return fallback

    return _get_from_env()


# =========================
# 🌍 ENV FALLBACK
# =========================
def _get_from_env() -> bool:
    val = _parse_bool(os.getenv("USE_AI", "false"))
    logger.debug(f"[AI CHECK] ENV → {val}")
    return val


# =========================
# 🧠 BOOL PARSER
# =========================
def _parse_bool(value: str) -> bool:
    if not value:
        return False
    return value.strip().lower() in {"true", "1", "yes", "on"}


# =========================
# ⚡ LOCAL CACHE UPDATE
# =========================
def _update_local_cache(value: bool):
    with LOCAL_LOCK:
        LOCAL_FALLBACK["value"] = value
        LOCAL_FALLBACK["ts"] = time.time()


# =========================
# 🧹 CACHE INVALIDATION
# =========================
def invalidate_ai_cache():
    cache.delete(CACHE_KEY)
    with LOCAL_LOCK:
        LOCAL_FALLBACK["value"] = None
        LOCAL_FALLBACK["ts"] = 0

    logger.info("[AI CHECK] Cache invalidated")