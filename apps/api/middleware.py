from django.http import JsonResponse
from .models import APIKey


class APIKeyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # ✅ Allow preflight requests (important for browser)
        if request.method == "OPTIONS":
            return self.get_response(request)

        # 🔥 Apply only on API routes
        if request.path.startswith("/api/"):

            # 🔥 CSRF bypass (MAIN FIX)
            request._dont_enforce_csrf_checks = True

            # 🔥 Read API key (multiple support)
            key = (
                request.headers.get("x-api-key") or
                request.headers.get("X-API-KEY") or
                request.META.get("HTTP_X_API_KEY")
            )

            # 🔥 Authorization Bearer support
            if not key:
                auth = request.headers.get("Authorization") or request.META.get("HTTP_AUTHORIZATION")
                if auth and auth.startswith("Bearer "):
                    key = auth.split(" ")[1]

            # ❌ Missing key
            if not key:
                return JsonResponse(
                    {"error": "API key missing"},
                    status=403
                )

            key = key.strip()

            # ❌ Invalid key
            if not APIKey.objects.filter(key=key, is_active=True).exists():
                return JsonResponse(
                    {"error": "Invalid API key"},
                    status=403
                )

        return self.get_response(request)
