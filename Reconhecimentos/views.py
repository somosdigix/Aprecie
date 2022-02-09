from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator
from datetime import date
from rolepermissions.roles import assign_role, remove_role
from rolepermissions.decorators import has_role_decorator

from Login.models import Colaborador
from Reconhecimentos.models import Pilar, Reconhecimento, Feedback, Ciclo, LOG_Ciclo
from Reconhecimentos.services import Notificacoes
from Aprecie.apps import AprecieConfig

def reconhecer(requisicao):
  id_do_reconhecedor = requisicao.POST['id_do_reconhecedor']
  id_do_reconhecido = requisicao.POST['id_do_reconhecido']
  id_do_pilar = requisicao.POST['id_do_pilar']
  descritivo = requisicao.POST['descritivo']

  reconhecido = Colaborador.objects.get(id = id_do_reconhecido)
  reconhecedor = Colaborador.objects.get(id = id_do_reconhecedor)
  pilar = Pilar.objects.get(id = id_do_pilar)
  feedback = Feedback.objects.create(descritivo = descritivo)


  data_ultima_apreciacao = reconhecedor.obter_ultima_data_de_publicacao()

  if data_ultima_apreciacao != date.today(): 
    reconhecido.reconhecer(reconhecedor, pilar, feedback)
    definir_data_de_publicacao(id_do_reconhecedor)
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
  
@has_role_decorator('administrador')
def switch_administrador(requisicao):
    
    id_do_colaborador = requisicao.POST['id_do_colaborador']
    eh_administrador  = requisicao.POST['eh_administrador']

    eh_administrador = converte_boolean(eh_administrador)
    colaborador = Colaborador.objects.get(id = id_do_colaborador)

    if eh_administrador:
      assign_role(colaborador, 'administrador')
      colaborador.tornar_administrador()
      colaborador.save()
    
    else:
      remove_role(colaborador, 'administrador')
      colaborador.remover_administrador()
      colaborador.save()

    return JsonResponse({})
   
def converte_boolean(bool):
    if bool.lower() == 'false':
        return False
    elif bool.lower() == 'true':
        return True
    else:
        raise ValueError("...")

def ultima_data_de_publicacao(requisicao, id_do_reconhecedor):
  reconhecedor = Colaborador.objects.get(id = id_do_reconhecedor)

  ultima_data = reconhecedor.obter_ultima_data_de_publicacao()

  resposta = {
    'ultima_data': ultima_data
  }

  return JsonResponse(resposta)

def definir_data_de_publicacao(id_do_reconhecedor):
  reconhecedor = Colaborador.objects.get(id = id_do_reconhecedor)

  reconhecedor.definir_ultima_data_de_publicacao(date.today())

  return JsonResponse ({})

def reconhecimentos_do_colaborador(requisicao, id_do_reconhecido):
  reconhecido = Colaborador.objects.get(id = id_do_reconhecido)
  pilares = list(map(lambda pilar: {
    'id': pilar.id,
    'nome': pilar.nome,
    'descricao': pilar.descricao,
    'possui_reconhecimentos': len(reconhecido.reconhecimentos_por_pilar(pilar)) > 0,
    'quantidade_de_reconhecimentos': len(reconhecido.reconhecimentos_por_pilar(pilar))
  }, Pilar.objects.all()))

  return JsonResponse({ 'id': reconhecido.id, 'nome': reconhecido.nome_abreviado, 'administrador': reconhecido.administrador, 'pilares': pilares }, safe = False)

def contar_reconhecimentos(requisicao):
   colaboradores = map(lambda colaborador: { 
     'nome': colaborador.nome_abreviado, 
     'apreciacoes': colaborador.contar_todos_reconhecimentos(), 
     'foto': colaborador.foto
     }, sorted(Colaborador.objects.all(), key=lambda x: x.contar_todos_reconhecimentos(), reverse=True)[:10])

   return JsonResponse({'colaboradores': list(colaboradores)})

def reconhecimentos_por_reconhecedor(requisicao, id_do_reconhecido):
  reconhecedores = Reconhecimento.objects.filter(reconhecido = id_do_reconhecido) \
    .values('reconhecedor__nome', 'reconhecedor', 'reconhecedor__id', 'pilar__id') \
    .annotate(quantidade_de_reconhecimentos=Count('reconhecedor'))

  for reconhecedor in reconhecedores:
    reconhecedor['reconhecedor__nome'] = Colaborador.obter_primeiro_nome(reconhecedor['reconhecedor__nome'])

  return JsonResponse({ 'reconhecedores': list(reconhecedores) })

def todas_as_apreciacoes(requisicao, id_do_reconhecido):
  reconhecido = Colaborador.objects.get(id=id_do_reconhecido)

  apreciacoes = map(lambda apreciacao: {
    'id': apreciacao.id,
    'data': apreciacao.data,
    'pilar__nome': apreciacao.pilar.nome,
    'feedback__descritivo': apreciacao.feedback.descritivo, 
    'reconhecedor__nome': apreciacao.reconhecedor.nome_abreviado,
    'reconhecedor__id': apreciacao.reconhecedor.id,
    'reconhecido__nome': apreciacao.reconhecido.nome_abreviado
  }, reconhecido.reconhecimentos().order_by('-id'))

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

def definir_ciclo(requisicao):
  data_inicial = requisicao.POST["data_inicial"]
  data_final = requisicao.POST["data_final"]
  id_usuario_que_modificou = requisicao.POST["usuario_que_modificou"]

  ciclo = Ciclo(data_inicial=data_inicial, data_final= data_final)
  ciclo.save()

  usuario_que_modificou = Colaborador.objects.get(id=id_usuario_que_modificou)
  log_Ciclo = LOG_Ciclo(ciclo=ciclo, usuario_que_modificou=usuario_que_modificou,descricao_da_alteracao='Criação do ciclo')
  log_Ciclo.save()

  return JsonResponse({})


def alterar_ciclo(requisicao):
  id_ciclo = requisicao.POST["id_ciclo"]
  data_final = requisicao.POST["data_final"]
  id_usuario_que_modificou = requisicao.POST["usuario_que_modificou"]
  descricao_da_alteracao = requisicao.POST["descricao_da_alteracao"]
  
  ciclo = Ciclo.objects.get(id = id_ciclo)
  ciclo.alterar_ciclo(data_final)
  ciclo.save()
  
  usuario_que_modificou = Colaborador.objects.get(id=id_usuario_que_modificou)
  log_Ciclo = LOG_Ciclo(ciclo = ciclo, usuario_que_modificou = usuario_que_modificou, descricao_da_alteracao = descricao_da_alteracao)
  log_Ciclo.save()

  return JsonResponse({})


def obter_ciclos(requisicao):
  resposta = {
    'ciclo_atual': obter_ciclo_atual(),
    'ciclos_anteriores': Ciclo.objects.all()
  }

  return JsonResponse(resposta)


def obter_ciclo_atual():
  try:
    return Ciclo.objects.get(data_final__gte=date.today(), data_inicial__lte=date.today())
  except Ciclo.DoesNotExist:
    return Ciclo.objects.get(data_final__isnull=True, data_inicial__lte=date.today())

@has_role_decorator('administrador')
def obter_notificacoes_do_administrador(requisicao):
  mensagem = AprecieConfig.obter_mensagem_notificacao()
  if mensagem != "":
    return JsonResponse(status=300, data={ 'mensagem': mensagem })
  else:
    return JsonResponse({})

  