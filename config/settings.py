from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 SECURITY
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-fallback")
DEBUG = os.getenv("DEBUG", "False") == "True"

# ✅ HOSTS
ALLOWED_HOSTS = ["*"]  # production me restrict karna

# 🧠 FEATURE FLAGS
USE_AI = os.getenv("USE_AI", "False") == "True"
AI_PROVIDER = os.getenv("AI_PROVIDER", "dummy")

# 🔑 API KEYS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🧠 APPLICATIONS
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

# ⚙️ MIDDLEWARE (🔥 ORDER FIXED)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # 🔥 API KEY middleware पहले
    'apps.api.middleware.APIKeyMiddleware',

    # 🔥 CSRF बाद में
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🌐 URL
ROOT_URLCONF = 'config.urls'

# 🎨 TEMPLATES
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

# 🚀 WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# 💾 DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🌍 LANGUAGE
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# 📦 STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 🔥 PROXY FIX
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 🔥 CSRF TRUST
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "http://localhost",
    "https://pawan.aspirantveda.in",   # 🔥 add domain
]

# 🔥 DRF SETTINGS (CSRF avoid)
REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],  # 🔥 disable session auth
}

# 🧠 DEFAULT PK
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
