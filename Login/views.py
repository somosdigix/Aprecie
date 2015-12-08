from datetime import datetime
from Login.models import Funcionario
from Login.services import ServicoDeAutenticacao
from django.http import JsonResponse

def entrar(requisicao):
	cpf = requisicao.POST['cpf']
	data_de_nascimento = datetime.strptime(requisicao.POST['data_de_nascimento'], '%d/%m/%Y')

	colaborador_autenticado = ServicoDeAutenticacao().autenticar(cpf, data_de_nascimento)

	return JsonResponse({
		'id_do_colaborador': colaborador_autenticado.id,
		'nome_do_colaborador': colaborador_autenticado.primeiro_nome,
		'foto_do_colaborador': None,
	})

def alterar_foto(requisicao):
	id_do_colaborador = requisicao.POST['id_do_colaborador']
	nova_foto = requisicao.POST['nova_foto']

	colaborador = Funcionario.objects.get(pk=id_do_colaborador)
	colaborador.alterar_foto(nova_foto)
	colaborador.save()

	return JsonResponse({})

def obter_funcionarios(requisicao):
	teste = []
	colaboradores = Funcionario.objects.all()

	for colaborador in colaboradores:
		teste.append({ 'id': colaborador.id, 'nome': colaborador.nome_abreviado })

	return JsonResponse({ 'colaboradores': teste })
