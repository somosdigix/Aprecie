from django.http import JsonResponse
import pytz
from django.utils import timezone
from django.conf import settings
from Aprecie.base import ExcecaoDeDominio
from Login.models import Colaborador

class ProcessadorDeExcecao(object):

	def process_exception(self, requisicao, excecao):
		if type(excecao) is ExcecaoDeDominio:
			return JsonResponse({'sucesso': False, 'mensagem': excecao.args[0]}, status=403)

class TimezoneMiddleware(object):
	def process_request(self, requisicao):
		tzname = settings.TIME_ZONE
		if tzname:
			timezone.activate(pytz.timezone(tzname))
		else:
			timezone.deactivate()

class AutenticadorDeColaborador:

	def authenticate(self, cpf, data_de_nascimento):
		try:
			return Colaborador.objects.get(cpf=cpf, data_de_nascimento=data_de_nascimento)
		except Colaborador.DoesNotExist:
			return None

	def get_user(self, user_id):
		try:
			return Colaborador.objects.get(pk=user_id)
		except Colaborador.DoesNotExist:
			return None