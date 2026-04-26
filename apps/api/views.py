from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db import transaction
from django.core.cache import cache

from apps.engine.orchestrator import run_pipeline
from apps.posts.models import Post, SiteSettings

import re
import hashlib


# =========================
# 🌐 PAGE
# =========================
@login_required
def generate_page(request):
    return render(request, "generate.html")


# =========================
# 🔧 HELPERS
# =========================
def normalize_keyword(keyword):
    keyword = keyword.lower().strip()
    keyword = re.sub(r"\s+", " ", keyword)
    return keyword


def cache_key(keyword):
    return "gen:" + hashlib.md5(keyword.encode()).hexdigest()


def get_site_settings():
    return SiteSettings.objects.first()


def get_active_provider():
    s = get_site_settings()
    return s.ai_provider if s else "unknown"


def should_auto_publish(score):
    s = get_site_settings()
    return s and s.auto_publish and score >= s.min_score_to_publish


# =========================
# 📊 SEO METRICS
# =========================
def word_count(text):
    return len(re.findall(r"\w+", text))


def keyword_density(text, keyword):
    total = len(text.split())
    if total == 0:
        return 0
    return round((text.lower().count(keyword.lower()) / total) * 100, 2)


def readability_score(text):
    sentences = text.split(".")
    words = text.split()
    if not sentences or not words:
        return 0
    return round(len(words) / len(sentences), 2)


# =========================
# 📦 RESPONSE
# =========================
def build_response(post, logs):
    return {
        "title": post.title,
        "content": post.content,
        "keyword": post.keyword,
        "score": post.score,
        "slug": post.slug,
        "word_count": word_count(post.content),
        "keyword_density": keyword_density(post.content, post.keyword),
        "readability": readability_score(post.content),
        "is_published": post.is_published,
        "provider": post.provider,
        "logs": logs or []
    }


# =========================
# 🚀 RATE LIMIT (ADVANCED)
# =========================
def is_rate_limited(user, ip):
    key = f"rate:{user.id}:{ip}"
    count = cache.get(key, 0)

    if count >= 10:
        return True

    cache.set(key, count + 1, 60)
    return False


# =========================
# 🤖 GENERATION CORE
# =========================
def generate_content(keyword):

    result = run_pipeline(keyword)

    if not result or not hasattr(result, "article"):
        raise Exception("Pipeline failed")

    article = result.article or {}

    content = article.get("content", "")

    # 🔁 retry if weak
    if len(content) < 200:
        result = run_pipeline(keyword + " detailed guide")
        article = result.article or {}
        content = article.get("content", content)

    return result, article


# =========================
# 🚀 API
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_post(request):

    try:
        user = request.user
        ip = request.META.get("REMOTE_ADDR")

        keyword = normalize_keyword(request.data.get("keyword", ""))
        force = request.data.get("force", False)

        # =========================
        # 🚫 RATE LIMIT
        # =========================
        if is_rate_limited(user, ip):
            return Response({"error": "Rate limit exceeded"}, status=429)

        # =========================
        # 🧾 VALIDATION
        # =========================
        if not keyword or len(keyword) < 3:
            return Response({"error": "Invalid keyword"}, status=400)

        # =========================
        # ⚡ CACHE CHECK
        # =========================
        key = cache_key(keyword)

        if not force:
            cached = cache.get(key)
            if cached:
                return Response({"cached": True, **cached})

        # =========================
        # ⚡ DB CHECK
        # =========================
        if not force:
            existing = Post.objects.filter(keyword=keyword).order_by("-created_at").first()
            if existing:
                data = build_response(existing, [])
                cache.set(key, data, 300)
                return Response({"cached": True, **data})

        # =========================
        # 🤖 GENERATE
        # =========================
        result, article = generate_content(keyword)

        title = article.get("title") or f"{keyword} Guide 2026"
        content = article.get("content", "")
        meta = (article.get("meta_description") or "")[:160]
        source = article.get("source", "AI")
        score = getattr(result, "score", 0)

        provider = get_active_provider()

        # =========================
        # 💾 SAVE
        # =========================
        with transaction.atomic():

            post = Post.objects.create(
                title=title,
                content=content,
                keyword=keyword,
                source=source,
                provider=provider,
                meta_description=meta,
                score=score
            )

            if should_auto_publish(score):
                post.status = "published"
                post.is_published = True
                post.published_at = now()
                post.save()

        response_data = build_response(post, getattr(result, "logs", []))

        cache.set(key, response_data, 300)

        return Response(response_data)

    except Exception as e:
        return Response({"error": str(e)}, status=500)