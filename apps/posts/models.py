from django.db import models


# 📝 POST MODEL
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
        ("dummy", "Dummy"),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    keyword = models.CharField(max_length=255)

    # 🔥 SEO FIELDS (IMPORTANT)
    meta_description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    source = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES,
        default="DUMMY"
    )

    # 🔥 WHICH AI GENERATED THIS
    provider = models.CharField(
        max_length=20,
        choices=PROVIDER_CHOICES,
        default="dummy"
    )

    score = models.IntegerField(default=0)

    # 🔥 PUBLISH TRACKING
    is_published = models.BooleanField(default=False)
    published_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ⚙️ SITE SETTINGS (ADMIN CONTROL)
class SiteSettings(models.Model):

    use_ai = models.BooleanField(default=False)

    # 🔥 SELECT AI PROVIDER FROM ADMIN
    ai_provider = models.CharField(
        max_length=20,
        choices=[
            ("openai", "OpenAI"),
            ("gemini", "Gemini"),
            ("dummy", "Dummy"),
        ],
        default="dummy"
    )

    def save(self, *args, **kwargs):
        self.pk = 1   # 🔥 single row enforce
        super().save(*args, **kwargs)

    def __str__(self):
        return f"AI: {self.use_ai} | Provider: {self.ai_provider}"