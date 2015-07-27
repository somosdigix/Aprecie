from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from Login.models import Funcionario
from Reconhecimentos.models import Valor, Reconhecimento
from Reconhecimentos.statics import ValoresDaDigithoBrasil
from django.db.models import Count
import json
import locale

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
	locale.setlocale(locale.LC_TIME, 'ptb')

	reconhecimentos = Reconhecimento.objects.all().order_by('-data')[:10]

	reconhecimentos_mapeados = list(map(lambda reconhecimento: {
		'id_do_reconhecedor': reconhecimento.reconhecedor.id,
		'nome_do_reconhecedor': reconhecimento.reconhecedor.nome,
		'foto_do_reconhecedor': reconhecimento.reconhecedor.foto,
		'id_do_reconhecido': reconhecimento.reconhecido.id,
		'nome_do_reconhecido': reconhecimento.reconhecido.nome,
		'foto_do_reconhecido': reconhecimento.reconhecido.foto,
		'valor': reconhecimento.valor.nome,
		'justificativa': reconhecimento.justificativa,
		'data': reconhecimento.data.strftime('%d de %B de %Y - %H:%M')
	}, reconhecimentos))

	return JsonResponse(reconhecimentos_mapeados, safe=False)

def reconhecimentos_do_funcionario(requisicao, id_do_reconhecido):
	reconhecido = Funcionario.objects.get(id=id_do_reconhecido)
	valores = list(map(lambda valor: {
		'id': valor.id,
		'nome': valor.nome,	
		'quantidade_de_reconhecimentos': len(reconhecido.reconhecimentos_por_valor(valor))
	}, ValoresDaDigithoBrasil.todos))

	return JsonResponse({ 'id': reconhecido.id, 'nome': reconhecido.nome, 'foto': reconhecido.foto, 'valores': valores }, safe=False)

def reconhecimentos_por_reconhecedor(requisicao, id_do_reconhecido):
	reconhecedores = Reconhecimento.objects.filter(reconhecido=id_do_reconhecido) \
		.values('reconhecedor__nome', 'reconhecedor', 'reconhecedor__foto', 'valor__id') \
		.annotate(quantidade_de_reconhecimentos=Count('reconhecedor'))

	for reconhecedor in reconhecedores:
		reconhecedor['reconhecedor__nome'] = Funcionario.obter_primeiro_nome(reconhecedor['reconhecedor__nome'])

	return JsonResponse({'reconhecedores': list(reconhecedores)})