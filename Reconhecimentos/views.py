from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from Login.models import Funcionario
from Reconhecimentos.models import Valor, Reconhecimento
from Reconhecimentos.statics import ValoresDaDigithoBrasil
from django.db.models import Count
import json

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

def ultimos_reconhecimentos(requisicao):
	reconhecimentos = Reconhecimento.objects.all().order_by('-data')[:10]
	reconhecimentosMapeados = list(map(lambda reconhecimento: { 'nome_do_reconhecido': reconhecimento.reconhecido.nome, 'valor': reconhecimento.valor.nome, 'justificativa': reconhecimento.justificativa, 'data': reconhecimento.data.strftime('%d/%m/%Y - %H:%M') }, reconhecimentos))

	return JsonResponse(reconhecimentosMapeados, safe=False)

def reconhecimentos_do_funcionario(requisicao):
	reconhecido = Funcionario.objects.get(id=requisicao.GET['id_do_reconhecido'])
	valores = list(map(lambda valor: { 'id': valor.id, 'nome': valor.nome, 'quantidade_de_reconhecimentos': len(reconhecido.reconhecimentos_por_valor(valor)) }, ValoresDaDigithoBrasil.todos))

	return JsonResponse({ 'id': reconhecido.id, 'nome': reconhecido.nome, 'valores': valores }, safe=False)

def reconhecimentos_por_reconhecedor(requisicao):
	id_do_reconhecido = int(requisicao.GET["id_do_reconhecido"])
	reconhecedores = Reconhecimento.objects.filter(reconhecido=id_do_reconhecido).values('reconhecedor').annotate(quantidade_de_reconhecimentos=Count('reconhecedor'))
	dicio = {}
	for item in reconhecedores:
		dicio[item['reconhecedor']] = item['quantidade_de_reconhecimentos']
	return JsonResponse(dicio)

