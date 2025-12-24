"""
Django settings for universe project.
"""

from pathlib import Path
from datetime import timedelta
import os

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ .env 로드 (backend/.env)
load_dotenv(BASE_DIR / ".env")


# ✅ 보안/환경
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-change-me"  # 로컬 기본값 (배포 시 반드시 .env로)
)

DEBUG = os.getenv("DEBUG", "1") == "1"

# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
ALLOWED_HOSTS = ['*']

# ✅ CORS (Vue 프론트 허용)
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173"
).split(",")


# Application definition
INSTALLED_APPS = [
    # Django 기본
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # ✅ 외부 라이브러리
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",

    # ✅ 프로젝트 앱
    "accounts",
    "movies",
    "reviews",
    "recommends",
]

MIDDLEWARE = [
    # ✅ CORS는 최대한 위로 (CommonMiddleware보다 위)
    "corsheaders.middleware.CorsMiddleware",
    
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "universe.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "universe.wsgi.application"


# Database (지금은 sqlite로 MVP)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ✅ Custom User 모델
AUTH_USER_MODEL = "accounts.User"


# ✅ DRF / JWT
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # 기본 알고리즘/설정은 SimpleJWT 기본값 사용
}


# Password validation (기본 그대로)
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ✅ 국제화(한국 기준)
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True
# ✅ 외부 API 키(나중 단계에서 사용)
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
AUTH_USER_MODEL = "accounts.User"
import os
GMS_MODEL = os.getenv("GMS_MODEL", "gpt-4o-mini")  # 없으면 기본값
GMS_KEY = os.getenv("GMS_KEY")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@thecomet.local"
FRONTEND_BASE_URL = "http://localhost:5173"  # 프론트 주소



# 마이페이지
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'




import dj_database_url
import os

# 배포 환경(Render)에서는 PostgreSQL을 쓰고, 내 컴퓨터에서는 sqlite3를 씀
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
    
    
    