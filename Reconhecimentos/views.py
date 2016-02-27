from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import formats
from Login.models import Colaborador
from Reconhecimentos.models import Valor, Reconhecimento
from django.db.models import Count

def reconhecer(requisicao):
	id_do_reconhecedor = requisicao.POST['id_do_reconhecedor']
	id_do_reconhecido = requisicao.POST['id_do_reconhecido']
	id_do_valor = requisicao.POST['id_do_valor']
	justificativa = requisicao.POST['justificativa']

	reconhecido = Colaborador.objects.get(id=id_do_reconhecido)
	reconhecedor = Colaborador.objects.get(id=id_do_reconhecedor)
	valor = Valor.objects.get(id=id_do_valor)

	reconhecido.reconhecer(reconhecedor, valor, justificativa)

	return JsonResponse({})

def ultimos_reconhecimentos(requisicao):
	reconhecimentos = Reconhecimento.objects.all().order_by('-data')[:10]

	reconhecimentos_mapeados = list(map(lambda reconhecimento: {
		'id_do_reconhecedor': reconhecimento.reconhecedor.id,
		'nome_do_reconhecedor': reconhecimento.reconhecedor.nome_abreviado,
		'id_do_reconhecido': reconhecimento.reconhecido.id,
		'nome_do_reconhecido': reconhecimento.reconhecido.nome_abreviado,
		'valor': reconhecimento.valor.nome,
		'justificativa': reconhecimento.justificativa,
		'data': reconhecimento.data
	}, reconhecimentos))

	return JsonResponse(reconhecimentos_mapeados, safe=False)

def reconhecimentos_do_colaborador(requisicao, id_do_reconhecido):
	reconhecido = Colaborador.objects.get(id=id_do_reconhecido)
	valores = list(map(lambda valor: {
		'id': valor.id,
		'nome': valor.nome,	
		'quantidade_de_reconhecimentos': len(reconhecido.reconhecimentos_por_valor(valor))
	}, Valor.objects.all()))

	return JsonResponse({ 'id': reconhecido.id, 'nome': reconhecido.nome_abreviado, 'valores': valores }, safe=False)

def reconhecimentos_por_reconhecedor(requisicao, id_do_reconhecido):
	reconhecedores = Reconhecimento.objects.filter(reconhecido=id_do_reconhecido) \
		.values('reconhecedor__nome', 'reconhecedor', 'reconhecedor__id', 'valor__id') \
		.annotate(quantidade_de_reconhecimentos=Count('reconhecedor'))

	for reconhecedor in reconhecedores:
		reconhecedor['reconhecedor__nome'] = Colaborador.obter_primeiro_nome(reconhecedor['reconhecedor__nome'])

	return JsonResponse({'reconhecedores': list(reconhecedores)})

def reconhecimentos_por_valor(requisicao, id_do_reconhecido, id_do_valor):
	reconhecido = Colaborador.objects.get(id=id_do_reconhecido)
	valor = Valor.objects.get(id=id_do_valor)
	reconhecimentos = reconhecido.reconhecimentos_por_valor(id_do_valor).values('data', 'justificativa', 'reconhecedor__nome', 'reconhecedor__id')
	resposta = {
		'id_do_valor': valor.id,
		'nome_do_valor': valor.nome,
		'id_do_reconhecido': reconhecido.id,
		'nome_do_reconhecido': reconhecido.nome_abreviado,
		'reconhecimentos': list(reconhecimentos)
	}

	return JsonResponse(resposta)
