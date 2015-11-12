from Aprecie import settings
from django.shortcuts import render

def index(requisicao):
	return render(requisicao, 'index.html', dict(eh_debug=not settings.ON_OPENSHIFT))