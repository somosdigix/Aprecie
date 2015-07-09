# -*- coding: utf-8 -*-
from datetime import datetime
from models import Funcionario
from django.http import JsonResponse

def entrar(requisicao):
	cpf = requisicao.POST['cpf']
	data_de_nascimento = datetime.strptime(requisicao.POST['data_de_nascimento'], '%d/%m/%Y')

	try:
		funcionario_autenticado = Funcionario.objects.get(cpf=cpf, data_de_nascimento=data_de_nascimento)
		return JsonResponse({
			'autenticado': True,
			'id_do_colaborador': funcionario_autenticado.id
		})
	except Funcionario.DoesNotExist:
		return JsonResponse({
		'autenticado': False,
		'mensagem': 'Colaborador não encontrado, confirme seus dados tente novamente'
	})

def obter_funcionarios(requisicao):
	termo = requisicao.GET['term']
	funcionarios = Funcionario.objects.filter(nome__icontains=termo)
	funcionarios = map(lambda funcionario: { 'id': funcionario.id, 'nome': funcionario.nome }, funcionarios)
	
	return JsonResponse(funcionarios, safe=False)