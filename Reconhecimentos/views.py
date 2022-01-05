from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import formats
from django.db.models import Count
from django.core.paginator import Paginator

from Login.models import Colaborador
from Reconhecimentos.models import Pilar, Reconhecimento, Feedback
from Reconhecimentos.services import Notificacoes

def reconhecer(requisicao):
  id_do_reconhecedor = requisicao.POST['id_do_reconhecedor']
  id_do_reconhecido = requisicao.POST['id_do_reconhecido']
  id_do_pilar = requisicao.POST['id_do_pilar']
  descritivo = requisicao.POST['descritivo']

  reconhecido = Colaborador.objects.get(id = id_do_reconhecido)
  reconhecedor = Colaborador.objects.get(id = id_do_reconhecedor)
  pilar = Pilar.objects.get(id = id_do_pilar)
  feedback = Feedback.objects.create(descritivo = descritivo)

  reconhecido.reconhecer(reconhecedor, pilar, feedback)
  Notificacoes.notificar_no_chat(reconhecedor, reconhecido, pilar)

  return JsonResponse({})

def ultimos_reconhecimentos(requisicao):
  reconhecimentos = Reconhecimento.objects.all().order_by('-id')

  pagina_atual = int(requisicao.GET['pagina_atual'])
  paginacao = Paginator(reconhecimentos, 10)
  pagina = paginacao.page(pagina_atual)

  reconhecimentos_mapeados = list(map(lambda reconhecimento: {
    'id': reconhecimento.pk,
    'id_do_reconhecedor': reconhecimento.reconhecedor.id,
    'nome_do_reconhecedor': reconhecimento.reconhecedor.nome_abreviado,
    'id_do_reconhecido': reconhecimento.reconhecido.id,
    'nome_do_reconhecido': reconhecimento.reconhecido.nome_abreviado,
    'pilar': reconhecimento.pilar.nome,
    'descritivo': reconhecimento.feedback.descritivo,
    'data': reconhecimento.data
  }, pagina.object_list))

  retorno = {
    'total_de_paginas': paginacao.num_pages,
    'pagina_atual': pagina.number,
    'reconhecimentos': reconhecimentos_mapeados
  }

  return JsonResponse(retorno, safe=False)

def reconhecimentos_do_colaborador(requisicao, id_do_reconhecido):
  reconhecido = Colaborador.objects.get(id = id_do_reconhecido)
  pilares = list(map(lambda pilar: {
    'id': pilar.id,
    'nome': pilar.nome,
    'descricao': pilar.descricao,
    'possui_reconhecimentos': len(reconhecido.reconhecimentos_por_pilar(pilar)) > 0,
    'quantidade_de_reconhecimentos': len(reconhecido.reconhecimentos_por_pilar(pilar))
  }, Pilar.objects.all()))

  return JsonResponse({ 'id': reconhecido.id, 'nome': reconhecido.nome_abreviado, 'pilares': pilares }, safe = False)

def reconhecimentos_por_reconhecedor(requisicao, id_do_reconhecido):
  reconhecedores = Reconhecimento.objects.filter(reconhecido = id_do_reconhecido) \
    .values('reconhecedor__nome', 'reconhecedor', 'reconhecedor__id', 'pilar__id') \
    .annotate(quantidade_de_reconhecimentos=Count('reconhecedor'))

  for reconhecedor in reconhecedores:
    reconhecedor['reconhecedor__nome'] = Colaborador.obter_primeiro_nome(reconhecedor['reconhecedor__nome'])

  return JsonResponse({ 'reconhecedores': list(reconhecedores) })

def todas_as_apreciacoes(requisicao, id_do_reconhecido):
  reconhecido = Colaborador.objects.get(id=id_do_reconhecido)
  
  apreciacoes = reconhecido.reconhecimentos() \
    .values('data', 'pilar__nome', 'feedback__descritivo', \
            'reconhecedor__nome', 'reconhecedor__id') \
    .order_by('-data', '-id')

  resposta = {
    'apreciacoes': list(apreciacoes)
  }

  return JsonResponse(resposta)

def todos_os_pilares_e_colaboradores(requisicao):
    pilares = map(lambda pilar: { 'id': pilar.id, 'nome': pilar.nome }, Pilar.objects.all())
    colaboradores = map(lambda colaborador: { 'id_colaborador': colaborador.id, 'nome': colaborador.nome_abreviado}, Colaborador.objects.all())

    retorno = {
      'pilares': list(pilares),
      'colaboradores': list(colaboradores)
    }

    return JsonResponse(retorno, safe=False)

def reconhecimentos_por_pilar(requisicao, id_do_reconhecido, id_do_pilar):
  reconhecido = Colaborador.objects.get(id=id_do_reconhecido)
  pilar = Pilar.objects.get(id=id_do_pilar)
  reconhecimentos = reconhecido.reconhecimentos_por_pilar(id_do_pilar) \
    .values('data', 'feedback__descritivo', \
            'reconhecedor__nome', 'reconhecedor__id') \
    .order_by('-data', '-id')

  resposta = {
    'id_do_pilar': pilar.id,
    'nome_do_pilar': pilar.nome,
    'descricao_do_pilar': pilar.descricao,
    'id_do_reconhecido': reconhecido.id,
    'nome_do_reconhecido': reconhecido.nome_abreviado,
    'reconhecimentos': list(reconhecimentos)
  }

  return JsonResponse(resposta)