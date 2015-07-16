from datetime import datetime
from Login.models import Funcionario
from Login.services import ServicoDeAutenticacao
from django.http import JsonResponse
from django.core import serializers

def entrar(requisicao):
	cpf = requisicao.POST['cpf']
	data_de_nascimento = datetime.strptime(requisicao.POST['data_de_nascimento'], '%d/%m/%Y')

	funcionario_autenticado = ServicoDeAutenticacao().autenticar(cpf, data_de_nascimento)

	return JsonResponse({
		'id_do_colaborador': funcionario_autenticado.id,
		'nome_do_colaborador': funcionario_autenticado.nome_compacto
	})

def obter_funcionarios(requisicao):
	funcionarios = serializers.serialize('json', Funcionario.objects.all(), fields=('id', 'nome_compacto'))
	return JsonResponse(funcionarios, safe=False)