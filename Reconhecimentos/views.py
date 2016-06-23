from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import formats
from Login.models import Colaborador
from Reconhecimentos.models import Valor, Reconhecimento, Feedback
from Reconhecimentos.services import Notificacoes
from django.db.models import Count

def reconhecer(requisicao):
	id_do_reconhecedor = requisicao.POST['id_do_reconhecedor']
	id_do_reconhecido = requisicao.POST['id_do_reconhecido']
	id_do_valor = requisicao.POST['id_do_valor']
	situacao = requisicao.POST['situacao']
	comportamento = requisicao.POST['comportamento']
	impacto = requisicao.POST['impacto']

	reconhecido = Colaborador.objects.get(id=id_do_reconhecido)
	reconhecedor = Colaborador.objects.get(id=id_do_reconhecedor)
	valor = Valor.objects.get(id=id_do_valor)
	feedback = Feedback.objects.create(situacao=situacao, comportamento=comportamento, impacto=impacto)

	reconhecido.reconhecer(reconhecedor, valor, feedback)
	Notificacoes.notificar_no_slack(reconhecedor, reconhecido, valor)

	return JsonResponse({})

def ultimos_reconhecimentos(requisicao):
	reconhecimentos = Reconhecimento.objects.all().order_by('-id')[:10]

	reconhecimentos_mapeados = list(map(lambda reconhecimento: {
		'id_do_reconhecedor': reconhecimento.reconhecedor.id,
		'nome_do_reconhecedor': reconhecimento.reconhecedor.nome_abreviado,
		'id_do_reconhecido': reconhecimento.reconhecido.id,
		'nome_do_reconhecido': reconhecimento.reconhecido.nome_abreviado,
		'valor': reconhecimento.valor.nome,
		'situacao': reconhecimento.feedback.situacao,
		'comportamento': reconhecimento.feedback.comportamento,
		'impacto': reconhecimento.feedback.impacto,
		'data': reconhecimento.data
	}, reconhecimentos))

	return JsonResponse(reconhecimentos_mapeados, safe=False)

def reconhecimentos_do_colaborador(requisicao, id_do_reconhecido):
	reconhecido = Colaborador.objects.get(id=id_do_reconhecido)
	valores = list(map(lambda valor: {
		'id': valor.id,
		'nome': valor.nome,
		'resumo': valor.resumo,
		'possui_reconhecimentos': len(reconhecido.reconhecimentos_por_valor(valor)) > 0,
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

# TODO: Método sem testes
def reconhecimentos_por_valor(requisicao, id_do_reconhecido, id_do_valor):
	reconhecido = Colaborador.objects.get(id=id_do_reconhecido)
	valor = Valor.objects.get(id=id_do_valor)
	reconhecimentos = reconhecido.reconhecimentos_por_valor(id_do_valor).values('data', 'feedback__situacao', 'feedback__comportamento', 'feedback__impacto', 'reconhecedor__nome', 'reconhecedor__id').order_by('-data')
	resposta = {
		'id_do_valor': valor.id,
		'nome_do_valor': valor.nome,
		'frases_de_descricao': valor.frases_de_descricao,
		'id_do_reconhecido': reconhecido.id,
		'nome_do_reconhecido': reconhecido.nome_abreviado,
		'reconhecimentos': list(reconhecimentos)
	}

	return JsonResponse(resposta)
