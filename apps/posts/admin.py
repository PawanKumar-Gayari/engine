from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse

from .models import Post, SiteSettings


# =========================
# 📝 POST ADMIN (ULTRA PRO DASHBOARD - FIXED)
# =========================
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "keyword",
        "status_badge",
        "seo_score_bar",
        "keyword_density_display",
        "rank_display",
        "provider",
        "open_post",
        "created_at",
    )

    list_filter = (
        "status",
        "provider",
        "source",
        "is_published",
        "created_at",
    )

    search_fields = ("title", "keyword", "slug")
    ordering = ("-created_at",)
    list_per_page = 25

    readonly_fields = (
        "created_at",
        "updated_at",
        "published_at",
        "slug_preview",
        "seo_score_bar",
        "keyword_density_display",
        "rank_display",
    )

    prepopulated_fields = {"slug": ("title",)}

    # =========================
    # ⚡ ACTIONS
    # =========================
    actions = [
        "publish_posts",
        "unpublish_posts",
        "reset_scores",
        "boost_scores",
    ]

    def publish_posts(self, request, queryset):
        updated = queryset.update(
            status="published",
            is_published=True,
            published_at=timezone.now()
        )
        self.message_user(request, f"🚀 {updated} posts published", messages.SUCCESS)

    def unpublish_posts(self, request, queryset):
        updated = queryset.update(
            status="draft",
            is_published=False,
            published_at=None
        )
        self.message_user(request, f"❌ {updated} posts unpublished", messages.WARNING)

    def reset_scores(self, request, queryset):
        updated = queryset.update(score=0, seo_score=0)
        self.message_user(request, f"♻️ {updated} scores reset", messages.INFO)

    def boost_scores(self, request, queryset):
        updated = queryset.update(seo_score=90)
        self.message_user(request, f"🔥 {updated} SEO boosted", messages.SUCCESS)

    # =========================
    # 🎨 VISUAL FIELDS (🔥 FIXED)
    # =========================

    @admin.display(description="Status")
    def status_badge(self, obj):
        color = "#28a745" if obj.is_published else "#dc3545"
        label = "Published" if obj.is_published else "Draft"

        return format_html(
            '<span style="background:{};color:white;padding:4px 10px;border-radius:6px;">{}</span>',
            color,
            label
        )

    @admin.display(description="SEO Score")
    def seo_score_bar(self, obj):
        score = obj.seo_score or 0

        if score >= 80:
            color = "#28a745"
        elif score >= 50:
            color = "#ffc107"
        else:
            color = "#dc3545"

        return format_html(
            '<div style="width:120px;background:#eee;border-radius:6px;">'
            '<div style="width:{}%;background:{};padding:4px;border-radius:6px;color:white;text-align:center;">'
            '{}'
            '</div></div>',
            score,
            color,
            score
        )

    @admin.display(description="Density")
    def keyword_density_display(self, obj):
        return f"{getattr(obj, 'keyword_density', 0) or 0}%"

    @admin.display(description="Rank")
    def rank_display(self, obj):
        score = getattr(obj, "rank_prediction", 0) or 0

        if score >= 80:
            return format_html('<b style="color:{};">🔥 {}</b>', "green", score)
        elif score >= 50:
            return format_html('<b style="color:{};">⚡ {}</b>', "orange", score)

        return format_html('<b style="color:{};">❌ {}</b>', "red", score)

    @admin.display(description="View")
    def open_post(self, obj):
        if obj.slug:
            return format_html(
                '<a href="/{}" target="_blank">🔗 Open</a>',
                obj.slug
            )
        return "-"

    @admin.display(description="Preview URL")
    def slug_preview(self, obj):
        return f"/{obj.slug}/" if obj.slug else "Not generated"

    # =========================
    # ⚡ PERFORMANCE
    # =========================
    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "title",
            "keyword",
            "status",
            "is_published",
            "provider",
            "score",
            "seo_score",
            "keyword_density",
            "rank_prediction",
            "slug",
            "created_at",
        )


# =========================
# ⚙️ SITE SETTINGS ADMIN
# =========================
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "use_ai",
        "ai_provider",
        "auto_publish",
        "min_score_to_publish",
        "enable_seo",
        "enable_rank_prediction",
    )

    list_display_links = ("ai_provider",)
    list_editable = ("use_ai", "auto_publish")

    fieldsets = (
        ("🧠 AI Control", {
            "fields": ("use_ai", "ai_provider")
        }),

        ("🚀 Auto Publish", {
            "fields": ("auto_publish", "min_score_to_publish")
        }),

        ("🔍 SEO Engine", {
            "fields": (
                "enable_seo",
                "enable_auto_fix",
                "enable_rank_prediction",
            )
        }),

        ("🌐 Site Settings", {
            "fields": ("site_name", "default_meta_description")
        }),

        ("⚡ Performance", {
            "fields": ("enable_cache",)
        }),

        ("🧩 Advanced", {
            "fields": ("default_schema",),
            "classes": ("collapse",),
        }),
    )