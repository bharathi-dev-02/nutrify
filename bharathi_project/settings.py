"""
Django settings for bharathi_project project.
"""

from pathlib import Path
import os

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m5+mx=vsk4)44#=wzb8ht1ev9rdms6a8s7h09z*h$j+p29!hhv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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
        ],  # ✅ Merged Both Template Paths
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

# ✅ Database Configuration for Multiple Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_bharathi',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': 'system',
        'PORT': '3306'
    },
    'da_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'da_db',
        'USER': 'root',
        'PASSWORD': 'system',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# ✅ Database Router to handle multiple databases
DATABASE_ROUTERS = ['bharathi_project.database_router.DatabaseRouter']

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store in DB
SESSION_COOKIE_AGE = 86400  # 1 day session expiration
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static & Media Files Configuration (Fixed)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "analysis", "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Collects static files for production

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # Stores uploaded files

# ✅ Ensure Unique File Paths to Prevent Collectstatic Errors
FILE_UPLOAD_PERMISSIONS = 0o644  # Ensures proper file read/write permissions

# ✅ Prevent duplicate static file names overriding each other
WHITENOISE_KEEP_ONLY_HASHED_FILES = True  # Only keep versioned static files

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ Razorpay API Keys
RAZORPAY_KEY_ID = "rzp_test_AciNtl2tzsXSNM"
RAZORPAY_KEY_SECRET = "PhVmK1Q5aOW54imScMYvwB1T"

