from datetime import datetime
from Login.models import Funcionario
from Login.services import ServicoDeAutenticacao
from django.http import JsonResponse

def entrar(requisicao):
	cpf = requisicao.POST['cpf']
	data_de_nascimento = datetime.strptime(requisicao.POST['data_de_nascimento'], '%d/%m/%Y')

	funcionario_autenticado = ServicoDeAutenticacao().autenticar(cpf, data_de_nascimento)

	return JsonResponse({
		'id_do_colaborador': funcionario_autenticado.id,
		'nome_do_colaborador': funcionario_autenticado.nome
	})

def obter_funcionarios(requisicao):
	funcionarios = Funcionario.objects.all()
	funcionarios = map(lambda funcionario: { 'id': funcionario.id, 'nome': funcionario.nome_compacto }, funcionarios)
	
	return JsonResponse(list(funcionarios), safe=False)