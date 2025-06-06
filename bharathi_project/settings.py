# bharathi_project/settings.py

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
import cloudinary

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security ---
SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-default-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# ✅ Fix CSRF Error: Ensure schema is present (http/https)
CSRF_TRUSTED_ORIGINS = [
    origin for origin in os.getenv('CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1:8000').split(',')
    if origin.startswith('http://') or origin.startswith('https://')
]

CORS_ALLOWED_ORIGINS = [
    origin for origin in os.getenv('CORS_ALLOWED_ORIGINS', 'http://127.0.0.1:8000').split(',')
    if origin.startswith('http://') or origin.startswith('https://')
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# --- Apps ---
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
    'cloudinary',
    'cloudinary_storage',
    'corsheaders',  # Add if using CORS
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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

# --- DATABASE CONFIG ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nutrify_db',
        'USER': 'root',
        'PASSWORD': 'system',
        'HOST': 'localhost',  # or cloud DB hostname
        'PORT': '3306',
    }
}




# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# --- Sessions ---
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static and Media ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'analysis', 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = f"https://res.cloudinary.com/{os.getenv('CLOUDINARY_CLOUD_NAME')}/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --- Cloudinary ---
cloudinary.config( 
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"), 
    api_key=os.getenv("CLOUDINARY_API_KEY"), 
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# --- Razorpay ---
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

# --- Default Field ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
