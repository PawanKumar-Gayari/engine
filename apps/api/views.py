from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.engine.orchestrator import run_pipeline
from apps.posts.models import Post


# 🌐 WEB PAGE (browser use)
def generate_page(request):
    return render(request, "generate.html")


# 🔥 API (CSRF + Auth disabled properly)
@csrf_exempt
@api_view(["POST"])
@authentication_classes([])   # 🔥 disable session auth (CSRF root cause)
@permission_classes([])       # 🔥 no permission needed (API key handles security)
def generate_post(request):

    keyword = request.data.get("keyword")

    if not keyword:
        return Response({"error": "Keyword required"}, status=400)

    try:
        # 🔥 ENGINE CALL
        result = run_pipeline(keyword)

        # 🛑 safety check
        if not result or not hasattr(result, "article"):
            return Response({"error": "Pipeline failed"}, status=500)

        article = result.article or {}

        # 🔍 SAFE GETS
        title = article.get("title", "No Title")
        content = article.get("content", "")
        source = article.get("source", "DUMMY")
        meta = article.get("meta_description", "")
        score = getattr(result, "score", 0)

        # 🔥 PROVIDER DETECT
        provider = "gemini" if source == "AI" else "dummy"

        # 💾 SAVE DB
        post = Post.objects.create(
            title=title,
            content=content,
            keyword=keyword,
            source=source,
            provider=provider,
            meta_description=meta,
            score=score
        )

        # 🚀 RESPONSE
        return Response({
            "message": "Generated via ENGINE",
            "title": post.title,
            "content": post.content,
            "source": post.source,
            "provider": post.provider,
            "score": post.score,
            "logs": getattr(result, "logs", [])
        })

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=500)
