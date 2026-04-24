from pathlib import Path
import os
from dotenv import load_dotenv

# =========================
# 📁 BASE DIR + ENV LOAD (FIXED)
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔥 IMPORTANT FIX (env सही load होगा)
load_dotenv(BASE_DIR / ".env")


# =========================
# 🔐 SECURITY
# =========================
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in .env")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")


# =========================
# 🧠 AI CONFIG
# =========================
USE_AI = os.getenv("USE_AI", "False") == "True"
AI_PROVIDER = os.getenv("AI_PROVIDER")

if USE_AI and not AI_PROVIDER:
    raise ValueError("AI_PROVIDER not set while USE_AI=True")


# 🔑 API KEYS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # 🔥 NEW


# 🔥 Safety check
if USE_AI:
    if AI_PROVIDER == "gemini" and not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY missing")

    if AI_PROVIDER == "openai" and not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY missing")

    if AI_PROVIDER == "openrouter" and not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY missing")  # 🔥 IMPORTANT


# =========================
# 🧠 APPLICATIONS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'apps.api',
    'apps.generator',
    'apps.posts',
    'apps.engine',
]


# =========================
# ⚙️ MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # 🔥 API KEY पहले
    'apps.api.middleware.APIKeyMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================
# 🌐 URL & TEMPLATES
# =========================
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# =========================
# 💾 DATABASE
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',

        # ✅ safe persistent db
        'NAME': os.getenv("DB_NAME", BASE_DIR / 'db.sqlite3'),
    }
}


# =========================
# 🌍 INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# =========================
# 📦 STATIC FILES
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =========================
# 🔥 PROXY / SECURITY
# =========================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "http://localhost",
    "https://pawan.aspirantveda.in",
]


# =========================
# 🔥 DRF SETTINGS
# =========================
REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
}


# =========================
# 🧠 DEFAULT PK
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'