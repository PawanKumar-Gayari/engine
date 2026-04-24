from django.http import JsonResponse
from .models import APIKey


class APIKeyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # ✅ Allow preflight requests
        if request.method == "OPTIONS":
            return self.get_response(request)

        # 🔥 Apply only on API routes
        if request.path.startswith("/api/"):

            # 🔥 Disable CSRF
            request._dont_enforce_csrf_checks = True

            # =========================
            # 🔑 READ API KEY
            # =========================
            key = (
                request.headers.get("x-api-key")
                or request.headers.get("X-API-KEY")
                or request.META.get("HTTP_X_API_KEY")
            )

            # 🔥 Authorization Bearer fallback
            if not key:
                auth = (
                    request.headers.get("Authorization")
                    or request.META.get("HTTP_AUTHORIZATION")
                )
                if auth and auth.startswith("Bearer "):
                    key = auth.split(" ")[1]

            # 🔍 DEBUG (temporary)
            print("🔑 RECEIVED KEY:", key)

            # ❌ Missing key
            if not key:
                return JsonResponse({"error": "API key missing"}, status=403)

            key = key.strip()

            # 🔍 DEBUG DB KEYS
            print("🔍 DB KEYS:", list(APIKey.objects.values_list("key", flat=True)))

            # =========================
            # ✅ VALIDATION
            # =========================
            if not APIKey.objects.filter(key__iexact=key, is_active=True).exists():
                return JsonResponse({"error": "Invalid API key"}, status=403)

        return self.get_response(request)
