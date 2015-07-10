# -*- coding: utf-8 -*-
from datetime import datetime
from models import Funcionario
from services import ServicoDeAutenticacao
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
	termo = requisicao.GET['term']
	funcionarios = Funcionario.objects.filter(nome__icontains=termo)
	funcionarios = map(lambda funcionario: { 'id': funcionario.id, 'nome': funcionario.nome }, funcionarios)
	
	return JsonResponse(funcionarios, safe=False)