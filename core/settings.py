import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


# ===============================
# 🔒 SÉCURITÉ
# ===============================
SECRET_KEY = os.environ.get('SECRET_KEY', 'unsafe-key-dev')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']


# ===============================
# 📦 APPS
# ===============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'platform_invest',
]


# ===============================
# ⚙️ MIDDLEWARE
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # 🔥 IMPORTANT (production)
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'core.urls'


# ===============================
# 🎨 TEMPLATES
# ===============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'


# ===============================
# 🗄️ DATABASE
# ===============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # dev
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 👉 PLUS TARD (PROD)
# PostgreSQL recommandé


# ===============================
# 🌍 LANGUES
# ===============================
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Africa/Luanda'

USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('fr', _('Français')),
    ('pt', _('Português')),
    ('en', _('English')),
]

LOCALE_PATHS = [BASE_DIR / 'locale']


# ===============================
# 📁 STATIC / MEDIA
# ===============================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_ROOT = BASE_DIR / 'staticfiles'  # prod

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ===============================
# 🔐 AUTH
# ===============================
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'


# ===============================
# 🔒 SÉCURITÉ AVANCÉE (PROD)
# ===============================
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    X_FRAME_OPTIONS = 'DENY'

    SECURE_SSL_REDIRECT = True


# ===============================
# ⚙️ DEFAULT
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
