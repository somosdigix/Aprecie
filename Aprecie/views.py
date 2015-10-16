from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings

def index(requisicao):
	template = loader.get_template('index.html')
	context = RequestContext(requisicao, {
		'eh_debug': settings.DEBUG
	})

	return HttpResponse(template.render(context))