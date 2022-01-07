from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import formats
from django.db.models import Count
from django.core.paginator import Paginator

from operator import attrgetter
from Login.models import Colaborador
from Reconhecimentos.models import Pilar, Reconhecimento, Feedback
from Reconhecimentos.services import Notificacoes

from datetime import date, datetime

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

def contar_reconhecimentos(requisicao):
   colaboradores = Colaborador.objects.all()[:10]

   transformacao = lambda colaborador: { 'nome': colaborador.nome_abreviado, 'apreciacoes': colaborador.contar_todos_reconhecimentos(), 'foto': colaborador.foto}
   colaboradores = map(transformacao, colaboradores)
   
   colaboradoresOrdenados= sorted(colaboradores, key=lambda x: x["apreciacoes"], reverse=True)

   return JsonResponse({'colaboradores': list(colaboradoresOrdenados)})


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
            'reconhecedor__nome', 'reconhecedor__id', 'reconhecido__nome') \
    .order_by('-data', '-id')

  resposta = {
    'apreciacoes': list(apreciacoes)
  }

  return JsonResponse(resposta)

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

def ranking_por_periodo(requisicao):
    data_inicio = requisicao.POST['data_inicio']
    data_fim = requisicao.POST['data_fim']
    
    colaboradores = Colaborador.objects.all()

    transformacao = lambda colaborador : { 
      'nome' : colaborador.nome_abreviado,
      'todos_reconhecimentos' : len(colaborador.reconhecimentos_por_data(converterData(data_inicio), converterData(data_fim))),
      'colaborar_sempre': len(colaborador.reconhecimentos_por_pilar_ranking(Pilar.objects.get(nome = "Colaborar sempre"), colaborador.reconhecimentos_por_data(converterData(data_inicio), converterData(data_fim)))),
      'focar_nas_pessoas': len(colaborador.reconhecimentos_por_pilar_ranking(Pilar.objects.get(nome = "Focar nas pessoas"), colaborador.reconhecimentos_por_data(converterData(data_inicio), converterData(data_fim)))),
      'fazer_diferente': len(colaborador.reconhecimentos_por_pilar_ranking(Pilar.objects.get(nome = "Fazer diferente"), colaborador.reconhecimentos_por_data(converterData(data_inicio), converterData(data_fim)))),
      'planejar_entregar_aprender': len(colaborador.reconhecimentos_por_pilar_ranking(Pilar.objects.get(nome = "Planejar, entregar e aprender"), colaborador.reconhecimentos_por_data(converterData(data_inicio), converterData(data_fim)))),
      'foto': colaborador.foto
    }
    
    colaboradores = map(transformacao, colaboradores)

    colaboradoresOrdenados = sorted(colaboradores, key=lambda x: x["todos_reconhecimentos"], reverse=True)
    
    return JsonResponse({'colaboradores': list(colaboradoresOrdenados)})

def converterData(data):
  return datetime.strptime(data, "%Y-%m-%d").date()



