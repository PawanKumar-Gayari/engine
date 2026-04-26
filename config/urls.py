from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from django.db import connection
from django.contrib.auth.decorators import login_required

from apps.api.views import generate_page  # ✅ IMPORTANT

import time


# =========================
# 🏠 HOME DASHBOARD
# =========================
def home(request):
    return HttpResponse(f"""
    <h2>🚀 AI Content Engine</h2>

    <p>Status: <b style="color:green;">LIVE</b></p>
    <p>Environment: <b>{'DEV' if settings.DEBUG else 'PRODUCTION'}</b></p>

    <hr>

    <ul>
        <li><a href="/admin/">🔐 Admin Panel</a></li>
        <li><a href="/generate/">⚡ Generator UI</a></li>
        <li><a href="/api/v1/">📡 API v1</a></li>
        <li><a href="/health/">❤️ Health</a></li>
        <li><a href="/metrics/">📊 Metrics</a></li>
    </ul>
    """)


# =========================
# ❤️ HEALTH CHECK
# =========================
def health(request):

    db_status = "ok"

    try:
        connection.cursor()
    except Exception:
        db_status = "error"

    return JsonResponse({
        "status": "ok",
        "service": "AI Content Engine",
        "env": "dev" if settings.DEBUG else "prod",
        "database": db_status,
        "ai_enabled": getattr(settings, "USE_AI", False)
    })


# =========================
# 🧠 READINESS
# =========================
def ready(request):
    return JsonResponse({
        "ready": True,
        "timestamp": time.time()
    })


# =========================
# 📊 METRICS
# =========================
def metrics(request):
    return JsonResponse({
        "uptime": "running",
        "debug": settings.DEBUG,
    })


# =========================
# ❌ ERROR HANDLERS
# =========================
def custom_404(request, exception):
    return JsonResponse({
        "error": "Route not found",
        "path": request.path
    }, status=404)


def custom_500(request):
    return JsonResponse({
        "error": "Internal server error"
    }, status=500)


# =========================
# 🌐 URLS
# =========================
urlpatterns = [

    # 🏠 Home
    path('', home, name="home"),

    # 🔐 Admin
    path('admin/', admin.site.urls),

    # =========================
    # 🌐 GENERATOR UI (FIXED ✅)
    # =========================
    path('generate/', login_required(generate_page), name="generate"),

    # =========================
    # 🔥 API VERSIONING
    # =========================
    path('api/v1/', include(('apps.api.urls', 'api'), namespace='api_v1')),

    # 🔁 backward support
    path('api/', include('apps.api.urls')),

    # =========================
    # ❤️ SYSTEM ENDPOINTS
    # =========================
    path('health/', health, name="health"),
    path('ready/', ready, name="ready"),
    path('metrics/', metrics, name="metrics"),
]


# =========================
# 📦 STATIC / MEDIA (DEV)
# =========================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# =========================
# ⚠️ ERROR HANDLERS
# =========================
handler404 = 'config.urls.custom_404'
handler500 = 'config.urls.custom_500'