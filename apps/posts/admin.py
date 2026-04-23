from django.contrib import admin
from .models import Post, SiteSettings


# 📝 POST ADMIN
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "keyword",
        "status",
        "source",
        "provider",
        "score",
        "is_published",
        "created_at",
    )

    list_filter = (
        "status",
        "source",
        "provider",
        "is_published",
        "created_at",
    )

    search_fields = ("title", "keyword")

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("📝 Content", {
            "fields": ("title", "content", "keyword")
        }),

        ("🔍 SEO", {
            "fields": ("meta_description", "slug")
        }),

        ("⚙️ Status", {
            "fields": ("status", "source", "provider", "score")
        }),

        ("🚀 Publishing", {
            "fields": ("is_published", "published_url")
        }),

        ("⏱ Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )


# ⚙️ SITE SETTINGS ADMIN
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    list_display = ("use_ai", "ai_provider")

    fieldsets = (
        ("🧠 AI Control", {
            "fields": ("use_ai", "ai_provider")
        }),
    )