from django.http import JsonResponse

class ProcessadorDeExcecao(object):

	def process_exception(self, requisicao, excecao):
		return JsonResponse({
			'sucesso': False,
			'mensagem': excecao.message
		}, status=403)