from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import formats
from django.db.models import Count
from django.core.paginator import Paginator
from datetime import date

from operator import attrgetter
from Login.models import Colaborador
from Reconhecimentos.models import Pilar, Reconhecimento, Feedback, Ciclo, LOG_Ciclo
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

def ultima_data_de_publicacao(requisicao, id_do_reconhecedor):
  reconhecedor = Colaborador.objects.get(id = id_do_reconhecedor)

  ultima_data = reconhecedor.obter_ultima_data_de_publicacao()

  resposta = {
    'ultimaData': ultima_data
  }

  return JsonResponse(resposta)

def definir_data_de_publicacao(requisicao, id_do_reconhecedor):
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

  return JsonResponse({ 'id': reconhecido.id, 'nome': reconhecido.nome_abreviado, 'pilares': pilares }, safe = False)

def contar_reconhecimentos(requisicao):
   colaboradores = map(lambda colaborador: { 
     'nome': colaborador.nome_abreviado, 
     'apreciacoes': colaborador.contar_todos_reconhecimentos(), 
     'foto': colaborador.foto
     }, Colaborador.objects.all()[:10])
   
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
  nome = requisicao.POST["nome_ciclo"]
  data_inicial = requisicao.POST["data_inicial"]
  data_final = requisicao.POST["data_final"]
  id_usuario_que_modificou = requisicao.POST["usuario_que_modificou"]

  ciclo = Ciclo(nome=nome, data_inicial=data_inicial, data_final= data_final)
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
  

def obter_informacoes_ciclo_atual(requisicao):
  ciclo = obter_ciclo_atual()
  log = LOG_Ciclo.objects.filter(ciclo=ciclo).order_by('-data_da_modificacao').first()
  colaborador = Colaborador.objects.get(id=log.usuario_que_modificou.id)

  resposta = {
    'id_ciclo': ciclo.id,
    'nome_do_ciclo': ciclo.nome,
    'data_inicial': ciclo.data_inicial,
    'data_inicial_formatada': ciclo.data_inicial.strftime('%d/%m/%Y'),
    'data_final': ciclo.data_final,
    'data_final_formatada': ciclo.data_final.strftime('%d/%m/%Y'),
    'nome_usuario_que_modificou': colaborador.nome_abreviado,
    'descricao_da_alteracao': log.descricao_da_alteracao,
    'data_ultima_alteracao': log.data_da_modificacao.strftime('%d/%m/%Y')
  }

  return JsonResponse(resposta)

def ciclos_passados(requisicao):
    ciclos_passados = map(lambda ciclo: { 'id_ciclo': ciclo.id, 'nome': ciclo.nome}, obter_ciclos_passados())

    lista_todos_ciclos_passados = list(ciclos_passados)
    numero_de_ciclos = len(lista_todos_ciclos_passados)

    secoes_teto = (numero_de_ciclos // 4)

    secoes_divisao_normal = (numero_de_ciclos / 4)

    if (secoes_divisao_normal % 2) != 0:
      secoes = secoes_teto + 1
      lista_por_secoes = cria_listas_de_ciclos(secoes, lista_todos_ciclos_passados)
    else: 
      secoes = secoes_divisao_normal
      lista_por_secoes = cria_listas_de_ciclos(secoes, lista_todos_ciclos_passados)

    resposta = {
			'ciclos_passados': lista_por_secoes
		}
  
    return JsonResponse(resposta, safe=False)

def cria_listas_de_ciclos(secoes, ciclos):
  lista_fragmentada_por_secoes = []

  for i in range(0, secoes): 
    lista_secao = []

    lista_secao.append(ciclos.pop(0))
    lista_secao.append(ciclos.pop(0))
    lista_secao.append(ciclos.pop(0))
    lista_secao.append(ciclos.pop(0))

    lista_fragmentada_por_secoes.append(lista_secao)

  return lista_fragmentada_por_secoes

def obter_ciclo_atual():
  return Ciclo.objects.get(data_final__gte=date.today(), data_inicial__lte=date.today())

def obter_ciclos_passados():
  return Ciclo.objects.filter(data_final__lte=date.today())