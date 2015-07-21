import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j@6p9^mw-rp$jwrk^hp7p@^cx=xo1siv**2!395vu@2rmd0z@8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'Login',
    'Reconhecimentos',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'Aprecie.middlewares.ProcessadorDeExcecao',
)

ROOT_URLCONF = 'Aprecie.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Aprecie.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Campo_Grande'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = '/static/'

ON_OPENSHIFT = "OPENSHIFT_APP_NAME" in os.environ

URL_DO_AMBIENTE = "aprecie.me"

if ON_OPENSHIFT:
    URL_DO_AMBIENTE = os.environ['OPENSHIFT_APP_DNS']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME':     os.environ['OPENSHIFT_APP_NAME'],
            'USER':     os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
            'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
            'HOST':     os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
            'PORT':     os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
        }
    }

    STATIC_ROOT = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'static')

