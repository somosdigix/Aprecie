import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'Valorometro'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'Valorometro.settings'

application = get_wsgi_application()