from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import re


# =========================
# 📝 POST MODEL (ULTRA SEO + AI READY)
# =========================
class Post(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    SOURCE_CHOICES = [
        ("AI", "AI"),
        ("DUMMY", "Dummy"),
    ]

    PROVIDER_CHOICES = [
        ("openai", "OpenAI"),
        ("gemini", "Gemini"),
        ("openrouter", "OpenRouter"),
        ("dummy", "Dummy"),
    ]

    # =========================
    # 🔥 CORE
    # =========================
    title = models.CharField(max_length=255)
    content = models.TextField()
    keyword = models.CharField(max_length=255, db_index=True)

    excerpt = models.TextField(blank=True, default="")

    # =========================
    # 🔥 SEO CORE
    # =========================
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        blank=True,
        null=True
    )

    meta_description = models.CharField(max_length=160, blank=True, default="")
    focus_keyword = models.CharField(max_length=255, blank=True, default="")
    tags = models.CharField(max_length=500, blank=True, default="")
    schema_json = models.JSONField(blank=True, null=True)
    canonical_url = models.URLField(blank=True, default="")

    # =========================
    # 📊 ADVANCED SEO METRICS (🔥 NEW)
    # =========================
    seo_score = models.IntegerField(default=0, db_index=True)
    keyword_density = models.FloatField(default=0)
    readability_score = models.IntegerField(default=0)
    rank_prediction = models.IntegerField(default=0)

    word_count = models.IntegerField(default=0)
    heading_count = models.IntegerField(default=0)

    # =========================
    # 🤖 AI INFO
    # =========================
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default="DUMMY")
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default="dummy")
    intent = models.CharField(max_length=50, blank=True, default="")

    # =========================
    # 📊 QUALITY SCORE
    # =========================
    score = models.PositiveIntegerField(default=0, db_index=True)

    # =========================
    # 🚀 PUBLISH
    # =========================
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_published = models.BooleanField(default=False, db_index=True)

    published_url = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)

    # =========================
    # ⏱️ TIME
    # =========================
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # =========================
    # 🔥 SAVE LOGIC (UPGRADED)
    # =========================
    def save(self, *args, **kwargs):

        self.title = (self.title or "").strip()

        # 🔹 slug
        if not self.slug:
            self.slug = self._generate_unique_slug(self.title)

        plain = self._strip_html(self.content)

        # 🔹 word count
        self.word_count = len(plain.split())

        # 🔹 heading count
        self.heading_count = self.content.lower().count("<h")

        # 🔹 meta
        if not self.meta_description:
            self.meta_description = (
                (plain[:157].rstrip() + "...")
                if len(plain) > 160 else plain
            )

        # 🔹 excerpt
        if not self.excerpt:
            self.excerpt = plain[:200].rstrip()

        # 🔹 focus keyword
        if not self.focus_keyword:
            self.focus_keyword = self.keyword

        # 🔹 keyword density (basic)
        if self.keyword:
            occurrences = plain.lower().count(self.keyword.lower())
            total_words = max(self.word_count, 1)
            self.keyword_density = round((occurrences / total_words) * 100, 2)

        # 🔹 canonical
        if not self.canonical_url and self.slug:
            self.canonical_url = f"/{self.slug}/"

        # 🔹 publish sync
        if self.status == "published":
            self.is_published = True
            if not self.published_at:
                self.published_at = timezone.now()
        else:
            self.is_published = False
            self.published_at = None

        super().save(*args, **kwargs)

    # =========================
    # 🔧 HELPERS
    # =========================
    def _generate_unique_slug(self, title):
        base = slugify(title)[:60] or "post"
        slug = base
        i = 1

        while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{i}"
            i += 1

        return slug

    def _strip_html(self, text):
        return re.sub(r"<[^>]+>", "", text or "")

    def __str__(self):
        return self.title


# =========================
# ⚙️ SITE SETTINGS (UPGRADED)
# =========================
class SiteSettings(models.Model):

    use_ai = models.BooleanField(default=False)

    ai_provider = models.CharField(
        max_length=20,
        choices=[
            ("openai", "OpenAI"),
            ("gemini", "Gemini"),
            ("openrouter", "OpenRouter"),
            ("dummy", "Dummy"),
        ],
        default="dummy"
    )

    site_name = models.CharField(max_length=255, default="My Blog")

    default_meta_description = models.CharField(max_length=160, blank=True, default="")

    # =========================
    # 🚀 AUTO PUBLISH CONTROL
    # =========================
    auto_publish = models.BooleanField(default=False)
    min_score_to_publish = models.PositiveIntegerField(default=70)

    # =========================
    # 🔥 SEO ENGINE TOGGLES
    # =========================
    enable_seo = models.BooleanField(default=True)
    enable_auto_fix = models.BooleanField(default=True)
    enable_rank_prediction = models.BooleanField(default=True)

    # =========================
    # ⚡ PERFORMANCE
    # =========================
    enable_cache = models.BooleanField(default=True)

    default_schema = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"AI: {self.use_ai} | Provider: {self.ai_provider}"