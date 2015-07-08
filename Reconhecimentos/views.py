from django.http import JsonResponse
from django.shortcuts import render
from Login.models import Funcionario
from Reconhecimentos.models import Valor
from Reconhecimentos.statics import ValoresDaDigithoBrasil
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def reconhecer(requisicao):
	id_do_reconhecedor = requisicao.POST['id_do_reconhecedor']
	id_do_reconhecido = requisicao.POST['id_do_reconhecido']
	id_do_valor = requisicao.POST['id_do_valor']
	justificativa = requisicao.POST['justificativa']

	reconhecido = Funcionario.objects.get(id=id_do_reconhecido)
	reconhecedor = Funcionario.objects.get(id=id_do_reconhecedor)
	valor = Valor.objects.get(id=id_do_valor)

	reconhecido.reconhecer(reconhecedor, valor, justificativa)

	return JsonResponse({})

@csrf_exempt
def reconhecimentos_do_funcionario(requisicao):
	funcionario = Funcionario.objects.get(cpf=requisicao.POST['cpf'])
	valores = map(lambda valor: { 'id': valor.id, 'nome': valor.nome, 'quantidade_de_reconhecimentos': len(funcionario.reconhecimentos_por_valor(valor)) }, ValoresDaDigithoBrasil.todos)

	return JsonResponse({ 'nome': funcionario.nome, 'cpf': funcionario.cpf, 'valores': valores }, safe=False)