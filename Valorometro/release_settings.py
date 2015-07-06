import os
from settings import *

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