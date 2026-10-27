from pathlib import Path
import os
from urllib.parse import urlparse
from django.contrib.messages import constants as message_constants
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-gerente-notas-troque-em-producao-xk3p9z'
)

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# URL publica do site no Render, ex.: https://gerente-notas.onrender.com
RENDER_URL = os.environ.get('RENDER_URL', '').strip().rstrip('/')

if RENDER_URL:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', urlparse(RENDER_URL).netloc]
else:
    ALLOWED_HOSTS = ['*']

# Necessário atrás do proxy HTTPS do Render (evita erro 403 CSRF no login)
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']
if RENDER_URL:
    CSRF_TRUSTED_ORIGINS.append(RENDER_URL)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
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

ROOT_URLCONF = 'gerente_notas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'gerente_notas.wsgi.application'

# ---------------------------------------------------------------------------
# Banco de dados: Supabase (PostgreSQL), via DATABASE_URL no .env.
# Sem DATABASE_URL, usa o PostgreSQL local (desenvolvimento).
# ---------------------------------------------------------------------------
_DATABASE_URL = os.environ.get('DATABASE_URL', '')

DATABASES = {
    'default': dj_database_url.config(
        default=_DATABASE_URL or 'postgresql://postgres:root@localhost:5432/Gerente_Notas',
        conn_max_age=600,
        ssl_require=bool(_DATABASE_URL),
    )
}

# API do Supabase (opcional - usada por core/supabase_client.py)
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')

# ---------------------------------------------------------------------------
# Redis: cache + sessoes. Sem REDIS_URL, usa cache em memoria local.
# ---------------------------------------------------------------------------
REDIS_URL = os.environ.get('REDIS_URL', '')

if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
            },
            'KEY_PREFIX': 'gerente_notas',
            'TIMEOUT': 300,
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
else:
    CACHES = {
        'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Fortaleza'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Bootstrap usa 'danger' (e não 'error') para alertas vermelhos
MESSAGE_TAGS = {message_constants.ERROR: 'danger'}
