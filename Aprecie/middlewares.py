from django.http import JsonResponse
import pytz
from django.utils import timezone
from django.conf import settings

class ProcessadorDeExcecao(object):

	def process_exception(self, requisicao, excecao):
		print("Excecao capturada: ", excecao)
		return JsonResponse({
			'sucesso': False,
			'mensagem': excecao.args[0]
		}, status=403)

class TimezoneMiddleware(object):
	def process_request(self, requisicao):
		tzname = settings.TIME_ZONE
		if tzname:
			timezone.activate(pytz.timezone(tzname))
		else:
			timezone.deactivate()