from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.engine.orchestrator import run_pipeline
from apps.posts.models import Post


@api_view(["POST"])
def generate_post(request):

    keyword = request.data.get("keyword")

    if not keyword:
        return Response({"error": "Keyword required"}, status=400)

    # 🔥 ENGINE CALL
    result = run_pipeline(keyword)
    article = result.article

    # 🔍 SAFE GETS
    title = article.get("title", "")
    content = article.get("content", "")
    source = article.get("source", "DUMMY")
    meta = article.get("meta_description", "")
    score = getattr(result, "score", 0)

    # 🔥 PROVIDER DETECT (simple logic)
    if source == "AI":
        provider = "gemini"  # default (later dynamic karenge)
    else:
        provider = "dummy"

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

    # 🚀 RESPONSE (DEBUG + PROOF)
    return Response({
        "message": "Generated via ENGINE",
        "title": post.title,
        "source": post.source,
        "provider": post.provider,
        "score": post.score,
        "logs": result.logs
    })