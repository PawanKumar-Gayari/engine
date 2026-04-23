from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


# 🔥 HOME PAGE
def home(request):
    return HttpResponse("🚀 AI Content Engine Running...")


urlpatterns = [
    path('', home),  # 👈 homepage added

    path('admin/', admin.site.urls),

    # 🔥 API routes
    path('api/', include('apps.api.urls')),
]
#yyddgit push origin main