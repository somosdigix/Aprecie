import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j@6p9^mw-rp$jwrk^hp7p@^cx=xo1siv**2!395vu@2rmd0z@8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
	'aprecie.herokuapp.com',
	'aprecie.digix.com.br',
	'temp.digix.com.br',
	'127.0.0.1'
]

INSTALLED_APPS = [
	'django.contrib.auth',
	'django.contrib.sessions',
	'django.contrib.contenttypes',
	'django.contrib.staticfiles',
	'Login',
	'Reconhecimentos',
	'compressor',
	'Aprecie.apps.AprecieConfig',
	'rolepermissions',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'Aprecie.middlewares.ProcessadorDeExcecao',
	'Aprecie.middlewares.TimezoneMiddleware',
	'Aprecie.middlewares.LoginObrigatorioMiddleware',
	'Aprecie.middlewares.PermiteUsoComTokenDeAdmin',
]

ROLEPERMISSIONS_MODULE = 'Login.roles'

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

AUTH_USER_MODEL = 'Login.Colaborador'
AUTHENTICATION_BACKENDS = ['Aprecie.middlewares.AutenticadorDeColaborador']

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
USE_L10N = True

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Campo_Grande'


USE_TZ = False

STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/') 

STATIC_URL = '/static/'

STATICFILES_DIRS = ()

IN_RELEASE_ENV = "APP_NAME" in os.environ

URL_DO_AMBIENTE = "aprecie.me"

COMPRESS_PRECOMPILERS = (
	('text/x-scss', 'sass --scss {infile} {outfile}'),
)

COMPRESS_ROOT = os.path.join(BASE_DIR, "static")

if IN_RELEASE_ENV:
	# URL_DO_AMBIENTE = os.environ['APP_DNS']
	ADMIN_TOKEN = os.environ['ADMIN_TOKEN']
	CHAT_WEBHOOK_URL_TEAMS = os.environ['CHAT_WEBHOOK_URL_TEAMS']

	db_from_env = dj_database_url.config(conn_max_age=500)
	DATABASES['default'].update(db_from_env)

	SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
	SECURE_SSL_REDIRECT = True
	# STATIC_ROOT = os.path.join(os.environ['REPO_DIR'], 'wsgi', 'static')
	# COMPRESS_ROOT = STATIC_ROOT
else:
	ADMIN_TOKEN = 'Basic dXN1YXJpb2xvY2FsOnNlbmhhbG9jYWw='
	CHAT_WEBHOOK_URL_TEAMS = ''


STATICFILES_FINDERS = (
	"django.contrib.staticfiles.finders.FileSystemFinder",
	"django.contrib.staticfiles.finders.AppDirectoriesFinder",
	'compressor.finders.CompressorFinder', 
)
