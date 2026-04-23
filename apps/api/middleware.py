from django.http import JsonResponse
from .models import APIKey


class APIKeyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith("/api/"):

            key = request.headers.get("x-api-key")

            if not key:
                return JsonResponse({"error": "API key missing"}, status=403)

            if not APIKey.objects.filter(key=key, is_active=True).exists():
                return JsonResponse({"error": "Invalid API key"}, status=403)

        return self.get_response(request)