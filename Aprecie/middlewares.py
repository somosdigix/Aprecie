from django.contrib.auth.backends import BaseBackend
from django.http import JsonResponse
import pytz
from django.utils import timezone
from django.conf import settings
from Aprecie.base import ExcecaoDeDominio
from Login.models import Colaborador
from Aprecie.base import acesso_anonimo, permite_acesso_anonimo

class ProcessadorDeExcecao(object):

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)

	def process_exception(self, requisicao, excecao):
		if type(excecao) is ExcecaoDeDominio:
			return JsonResponse({'sucesso': False, 'mensagem': excecao.args[0]}, status=403)

class TimezoneMiddleware(object):
	
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)

	def process_request(self, requisicao):
		tzname = settings.TIME_ZONE
		if tzname:
			timezone.activate(pytz.timezone(tzname))
		else:
			timezone.deactivate()

class AutenticadorDeColaborador(BaseBackend):

	def authenticate(self, request, cpf=None, data_de_nascimento=None):
		try:
			return Colaborador.objects.get(cpf=cpf, data_de_nascimento=data_de_nascimento)
		except:
			return None

	def get_user(self, user_id):
		try:
			return Colaborador.objects.get(pk=user_id)
		except:
			return None

class LoginObrigatorioMiddleware():

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)

	def process_view(self, request, view_func, view_args, view_kwarg):
		# print("Autenticado", request.user.is_authenticated())
		# print("permite_acesso_anonimo(view_func)", permite_acesso_anonimo(view_func))
		# if not request.user.is_authenticated() and not permite_acesso_anonimo(view_func):
		# 	print("USUARIO", request.user)
		# 	return HttpResponse('Unauthorized', status=401)
		pass

	def process_request(self, request):
		#print (request.user)
		pass
