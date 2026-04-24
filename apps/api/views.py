from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

from apps.engine.orchestrator import run_pipeline
from apps.posts.models import Post, SiteSettings


# =========================
# 🌐 WEB PAGE
# =========================
def generate_page(request):
    return render(request, "generate.html")


# =========================
# 🔧 HELPER FUNCTIONS
# =========================
def get_active_provider():
    settings = SiteSettings.objects.first()
    if settings and settings.ai_provider:
        return settings.ai_provider
    return "unknown"


def build_response(post, logs):
    return {
        "message": "Generated via ENGINE",
        "title": post.title,
        "content": post.content,
        "keyword": post.keyword,
        "source": post.source,
        "provider": post.provider,
        "score": post.score,
        "meta_description": post.meta_description,
        "created_at": post.created_at if hasattr(post, "created_at") else str(now()),
        "logs": logs or []
    }


# =========================
# 🚀 API ENDPOINT
# =========================
@csrf_exempt
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def generate_post(request):

    try:
        # =========================
        # 🧾 INPUT VALIDATION
        # =========================
        keyword = request.data.get("keyword", "").strip()

        if not keyword:
            return Response({
                "status": "error",
                "error": "Keyword is required"
            }, status=400)

        if len(keyword) < 2:
            return Response({
                "status": "error",
                "error": "Keyword too short"
            }, status=400)

        # =========================
        # 🤖 RUN ENGINE
        # =========================
        result = run_pipeline(keyword)

        if not result or not hasattr(result, "article"):
            return Response({
                "status": "error",
                "error": "Pipeline execution failed"
            }, status=500)

        article = result.article or {}

        # =========================
        # 📦 SAFE EXTRACTION
        # =========================
        title = article.get("title") or f"{keyword} - Complete Guide 2026"
        content = article.get("content") or ""
        source = article.get("source", "DUMMY")
        meta = article.get("meta_description", "")[:160]
        score = getattr(result, "score", 0)

        # =========================
        # 🔥 PROVIDER DETECTION
        # =========================
        provider = get_active_provider()

        # =========================
        # 💾 SAVE TO DATABASE
        # =========================
        post = Post.objects.create(
            title=title,
            content=content,
            keyword=keyword,
            source=source,
            provider=provider,
            meta_description=meta,
            score=score
        )

        # =========================
        # 🚀 SUCCESS RESPONSE
        # =========================
        return Response({
            "status": "success",
            **build_response(post, getattr(result, "logs", []))
        }, status=200)

    except Exception as e:
        # =========================
        # ❌ ERROR HANDLING
        # =========================
        return Response({
            "status": "error",
            "error": str(e)
        }, status=500)