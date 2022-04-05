﻿from django.http import JsonResponse
from django.db.models import Count
from Login.models import Colaborador
from Reconhecimentos.models import Pilar, Reconhecimento, Feedback
from Reconhecimentos.services import Notificacoes
from django.core.paginator import Paginator
from rolepermissions.decorators import has_role_decorator
from Aprecie.apps import AprecieConfig
from datetime import date, datetime

def reconhecer(requisicao):
  id_do_reconhecedor = requisicao.POST['id_do_reconhecedor']
  id_do_reconhecido = requisicao.POST['id_do_reconhecido']
  id_do_pilar = requisicao.POST['id_do_pilar']
  descritivo = requisicao.POST['descritivo']

  reconhecedor = Colaborador.objects.get(id = id_do_reconhecedor)
  
  if verificar_ultima_data_de_publicacao(reconhecedor):
    reconhecido = Colaborador.objects.get(id = id_do_reconhecido)
    pilar = Pilar.objects.get(id = id_do_pilar)
    feedback = Feedback.objects.create(descritivo = descritivo)
    reconhecido.reconhecer(reconhecedor, pilar, feedback)
    Notificacoes.notificar_no_chat(reconhecedor, reconhecido, pilar)
    definir_data_de_publicacao(reconhecedor)

    return JsonResponse({})

  else:
    return JsonResponse(status=403, data = {'mensagem': 'Você já fez um reconhecimento hoje, poderá fazer amanhã novamente!'})

def verificar_ultima_data_de_publicacao(reconhecedor):
  ultima_data = reconhecedor.obter_ultima_data_de_publicacao()

  return not(ultima_data == date.today())
  

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
  
def converte_boolean(bool):
    if bool.lower() == 'false':
        return False
    elif bool.lower() == 'true':
        return True
    else:
        raise ValueError("...")

def definir_data_de_publicacao(reconhecedor):
  reconhecedor.definir_ultima_data_de_publicacao(date.today())
  reconhecedor.save()

def reconhecimentos_do_colaborador(requisicao, id_do_reconhecido):
  reconhecido = Colaborador.objects.get(id = id_do_reconhecido)
  pilares = list(map(lambda pilar: {
    'id': pilar.id,
    'nome': pilar.nome,
    'descricao': pilar.descricao,
    'possui_reconhecimentos': len(reconhecido.reconhecimentos_por_pilar(pilar)) > 0,
    'quantidade_de_reconhecimentos': len(reconhecido.reconhecimentos_por_pilar(pilar))
  }, Pilar.objects.all()))

  resposta = {
    'id': reconhecido.id,
    'nome': reconhecido.nome_abreviado,
    'administrador': reconhecido.administrador,
    'pilares': pilares
  }

  return JsonResponse(resposta, safe = False)

def reconhecimentos_por_reconhecedor(requisicao, id_do_reconhecido):
  reconhecedores = Reconhecimento.objects.filter(reconhecido = id_do_reconhecido) \
    .values('reconhecedor__nome', 'reconhecedor', 'reconhecedor__id', 'pilar__id') \
    .annotate(quantidade_de_reconhecimentos=Count('reconhecedor'))

  for reconhecedor in reconhecedores:
    reconhecedor['reconhecedor__nome'] = Colaborador.obter_primeiro_nome(reconhecedor['reconhecedor__nome'])

  return JsonResponse({ 'reconhecedores': list(reconhecedores) })

def todas_as_apreciacoes(requisicao, id_do_reconhecido):
  reconhecido = Colaborador.objects.get(id=id_do_reconhecido)

  apreciacoes_recebidas = map(lambda apreciacao: {
    'id': apreciacao.id,
    'data': apreciacao.data,
    'pilar__nome': apreciacao.pilar.nome,
    'feedback__descritivo': apreciacao.feedback.descritivo, 
    'reconhecedor__nome': apreciacao.reconhecedor.nome_abreviado,
    'reconhecedor__id': apreciacao.reconhecedor.id,
    'reconhecido__nome': apreciacao.reconhecido.nome_abreviado
  }, reconhecido.reconhecimentos().order_by('-id'))

  apreciacoes_feitas = map(lambda apreciacao: {
    'id': apreciacao.id,
    'data': apreciacao.data,
    'pilar__nome': apreciacao.pilar.nome,
    'feedback__descritivo': apreciacao.feedback.descritivo, 
    'reconhecedor__nome': apreciacao.reconhecedor.nome_abreviado,
    'reconhecedor__id': apreciacao.reconhecedor.id,
    'reconhecido__nome': apreciacao.reconhecido.nome_abreviado
  }, Reconhecimento.objects.filter(reconhecedor = requisicao.user.id).order_by('-id'))

  apreciacoes = {
    'feitas': list(apreciacoes_feitas),
    'recebidas': list(apreciacoes_recebidas)
  }

  return JsonResponse(apreciacoes)

def todos_os_pilares_e_colaboradores(requisicao):
    pilares = map(lambda pilar: { 
      'id': pilar.id, 
      'nome': pilar.nome 
      }, Pilar.objects.all())

    colaboradores = map(lambda colaborador: { 
      'id_colaborador': colaborador.id, 
      'nome': colaborador.nome_abreviado
      }, Colaborador.objects.all())

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

def converterData(data):
  return datetime.strptime(data, "%Y-%m-%d").date()

@has_role_decorator('administrador')
def obter_notificacoes_do_administrador(requisicao):
  notificacao = AprecieConfig.obter_mensagem_notificacao()

  data = {
    'mensagem': notificacao
  }

  return JsonResponse(data)