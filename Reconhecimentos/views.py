from django.http import JsonResponse
from django.shortcuts import render
from Login.models import Funcionario
from Reconhecimentos.models import Valor
from Reconhecimentos.statics import ValoresDaDigithoBrasil
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def reconhecer(requisicao):
	cpf = requisicao.POST['cpf']
	valor_id = requisicao.POST['valor_id']
	justificativa = requisicao.POST['justificativa']

	funcionario = Funcionario.objects.get(cpf=cpf)
	valor = Valor.objects.get(id=valor_id)

	funcionario.reconhecer(valor, justificativa)

	return JsonResponse({})

@csrf_exempt
def reconhecimentos_do_funcionario(requisicao):
	funcionario = Funcionario.objects.get(cpf=requisicao.POST['cpf'])
	valores = map(lambda valor: { 'id': valor.id, 'nome': valor.nome, 'quantidade_de_reconhecimentos': len(funcionario.reconhecimentos_por_valor(valor)) }, ValoresDaDigithoBrasil.todos)

	return JsonResponse({ 'nome': funcionario.nome, 'cpf': funcionario.cpf, 'valores': valores }, safe=False)

@login_required
def escolher_elogiado(requisicao):
	return render(requisicao, "escolher_elogiado.html")