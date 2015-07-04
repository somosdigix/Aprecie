from django.http import JsonResponse
from django.shortcuts import render
from Login.models import Funcionario
from Reconhecimentos.models import Valor

def reconhecer(requisicao):
	cpf = requisicao.POST['cpf']
	idDoValor = requisicao.POST['idDoValor']
	justificativa = requisicao.POST['justificativa']

	funcionario = Funcionario.objects.get(cpf=cpf)
	valor = Valor.objects.get(id=idDoValor)

	funcionario.reconhecer(valor, justificativa)

	return JsonResponse({})