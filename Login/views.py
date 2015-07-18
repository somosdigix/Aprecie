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
		'nome_do_colaborador': colaborador_autenticado.nome_compacto,
		'foto_do_colaborador': colaborador_autenticado.foto
	})

def alterar_foto(requisicao):
	id_do_colaborador = requisicao.POST['id_do_colaborador']
	nova_foto = requisicao.POST['nova_foto']

	colaborador = Funcionario.objects.get(pk=id_do_colaborador)
	colaborador.alterar_foto(nova_foto)
	colaborador.save()

	return JsonResponse({})

def obter_funcionarios(requisicao):
	colaboradores = {
		'colaboradores': list(Funcionario.objects.all().values('id', 'nome'),)
	}

	return JsonResponse(colaboradores)
