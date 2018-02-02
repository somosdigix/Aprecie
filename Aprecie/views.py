from Aprecie import settings
from django.shortcuts import render
from Aprecie.base import acesso_anonimo
from django.http import HttpResponse

@acesso_anonimo
def index(requisicao):
	return render(requisicao, 'index.html', dict(eh_debug=not settings.ON_AZURE))

@acesso_anonimo
def login(requisicao):
	return render(requisicao, 'login.html', dict(eh_debug=not settings.ON_AZURE))

def home(request):
  html = "<html><body>Hello World!</body></html>"
  return HttpResponse(html)