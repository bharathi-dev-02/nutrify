"""
Django settings for bharathi_project project.
"""

from pathlib import Path
import os
import dj_database_url  # type: ignore
import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-m5+mx=vsk4)44#=wzb8ht1ev9rdms6a8s7h09z*h$j+p29!hhv')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ["nutrify.up.railway.app", "127.0.0.1", "localhost"]

CSRF_TRUSTED_ORIGINS = [
    "https://nutrify.up.railway.app"
]

CORS_ALLOWED_ORIGINS = [
    "https://nutrify.up.railway.app"
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'analysis',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bharathi_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'shop', 'templates'),
            os.path.join(BASE_DIR, 'analysis', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bharathi_project.wsgi.application'

# ✅ FIXED: MySQL Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'railway'),  # ✅ Default to 'railway'
        'USER': os.getenv('MYSQLUSER', 'root'),  # ✅ Default to 'root'
        'PASSWORD': os.getenv('MYSQLPASSWORD', 'cadnJAeyWhsEcQywFEVPdxyIWHcgcAaO'),  # ✅ Actual password
        'HOST': os.getenv('MYSQLHOST', 'shuttle.proxy.rlwy.net'),  # ✅ Actual host
        'PORT': os.getenv('MYSQLPORT', '19758'),  # ✅ MySQL default port
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# ✅ REMOVE if you don’t have database_router.py
# DATABASE_ROUTERS = ['bharathi_project.database_router.DatabaseRouter']

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 1 day session expiration
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static & Media Files Configuration
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "analysis", "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ Ensure Unique File Paths
FILE_UPLOAD_PERMISSIONS = 0o644
WHITENOISE_KEEP_ONLY_HASHED_FILES = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ Razorpay API Keys from Environment Variables
RAZORPAY_KEY_ID = os.getenv("rzp_test_AciNtl2tzsXSNM")
RAZORPAY_KEY_SECRET = os.getenv("PhVmk1Q5aOW54imScMYvwB1T")

