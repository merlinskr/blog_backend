"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 5.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-fa&-!aeu*l%9r2km)(50b+5a&$m*(j17h68gc1cvu-=12#i^7p"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),  # access token 1 天过期
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # refresh token 有效 7 天
    "ROTATE_REFRESH_TOKENS": True,  # 每次刷新后发新 refresh token
    "BLACKLIST_AFTER_ROTATION": True,  # 旧的 refresh token 作废
    "AUTH_HEADER_TYPES": ("Bearer",),  # 请求头加 Bearer: xxx
}

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",  # Django REST框架核心包，提供API开发功能
    "drf_spectacular",  # 自动生成API文档和Swagger界面
    "corsheaders",  # CORS中间件，解决跨域问题
    "accounts",  # 你的用户账户应用
    "article",  # 文章管理应用
]

REST_FRAMEWORK = {
    # 'EXCEPTION_HANDLER': 'blog.exceptions.custom_exception_handler',
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",  # 使用Spectacular自动生成API文档
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",  # 启用分页功能
    "PAGE_SIZE": 20,  # 每页显示20条记录
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Blog API",  # API文档标题
    "DESCRIPTION": "A blog application API",  # API描述
    "VERSION": "1.0.0",  # API版本号
    "SERVE_INCLUDE_SCHEMA": False,  # 不在文档中包含原始schema
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS中间件，必须放在最前面
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "blog.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mydb",
        "USER": "yulon",
        "PASSWORD": "!YulonGoStudy",
        "HOST": "118.178.237.131",
        "PORT": "3306",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 自定义用户模型
AUTH_USER_MODEL = "accounts.User"

# CORS配置
# 允许所有源进行跨域请求（开发环境）
CORS_ALLOW_ALL_ORIGINS = True

# 生产环境中应该使用具体的域名列表，例如：
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",      # React开发服务器
#     "http://127.0.0.1:3000",      # React开发服务器
#     "http://localhost:8080",      # Vue开发服务器
#     "https://yourdomain.com",     # 生产环境前端域名
# ]

# 允许的HTTP方法
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# 允许的请求头
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
