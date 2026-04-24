from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from apps.api.views import generate_page


# 🔥 HOME PAGE
def home(request):
    return HttpResponse("🚀 AI Content Engine Running...")


urlpatterns = [
    path('', home),

    # 🔐 Admin
    path('admin/', admin.site.urls),

    # 🔥 API routes
    path('api/', include('apps.api.urls')),

    # 🌐 Web UI (browser)
    path('generate/', generate_page),
]
