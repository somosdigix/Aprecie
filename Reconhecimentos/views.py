from inspect import CO_ASYNC_GENERATOR
from django.http import JsonResponse
from django.db.models import Count
from Login.models import Colaborador
from Reconhecimentos.models import Agradecimento, Pilar, Reconhecimento, Feedback, Ciclo, LOG_Ciclo
from Reconhecimentos.services import Notificacoes
from django.core.paginator import Paginator
from rolepermissions.decorators import has_role_decorator
from Aprecie.apps import AprecieConfig
from django.db import connection
from datetime import date, datetime, timedelta

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
    Notificacoes.notificar_no_chat_msteams(reconhecedor, reconhecido, pilar, descritivo)
    Notificacoes.notificar_no_chat_discord(reconhecedor, reconhecido, pilar)
    definir_data_de_publicacao(reconhecedor)

    return JsonResponse({})

  else:
    return JsonResponse(status=403, data = {'mensagem': 'Você já fez um reconhecimento hoje, poderá fazer amanhã novamente!'})

def verificar_ultima_data_de_publicacao(reconhecedor):
  ultima_data = reconhecedor.obter_ultima_data_de_publicacao()

  return not(ultima_data == date.today())
  
def agradecer(requisicao):
  
  id_reconhecimento_vinculado = requisicao.POST['id_reconhecimento_vinculado']
  id_colaborador_que_agradeceu = requisicao.POST['id_colaborador_que_agradeceu']
  mensagem = requisicao.POST['agradecimento']
 
  colaborador_que_agradeceu = Colaborador.objects.get(id=id_colaborador_que_agradeceu)
  reconhecimento_vinculado = Reconhecimento.objects.get(id=id_reconhecimento_vinculado)

  agradecimento = Agradecimento(colaborador=colaborador_que_agradeceu, reconhecimento=reconhecimento_vinculado, mensagem=mensagem)
  agradecimento.save()

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

def contar_reconhecimentos(requisicao):
   colaboradores = map(lambda colaborador: { 
     'nome': colaborador[2], 
     'apreciacoes': colaborador[0], 
     'foto': colaborador[3]
     }, obter_reconhecimentos_dos_colaboradores())

   return JsonResponse({'colaboradores': list(colaboradores)})

def obter_reconhecimentos_dos_colaboradores():
  with connection.cursor() as cursor:
    cursor.execute('''
      SELECT count(*), r.reconhecido_id, l.nome, l.foto
      FROM public."Reconhecimentos_reconhecimento" r
      JOIN public."Login_colaborador" l ON r.reconhecido_id = l.id
      GROUP by r.reconhecido_id, l.nome, l.foto
      ORDER by count(*) DESC, l.nome
      LIMIT 10
    ''')
    reconhecimentos = cursor.fetchall()
  return reconhecimentos

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
    'reconhecedor__id': apreciacao.reconhecedor.id,
    'reconhecedor__nome': apreciacao.reconhecedor.nome_abreviado,
    'reconhecido__id': apreciacao.reconhecido.id,
    'reconhecido__nome': apreciacao.reconhecido.nome_abreviado,
    'agradecimentos': obter_agradecimentos(apreciacao, apreciacao.reconhecido.id, apreciacao.reconhecedor.id)
  }, reconhecido.reconhecimentos().order_by('-id'))

  apreciacoes_feitas = map(lambda apreciacao: {
    'id': apreciacao.id,
    'data': apreciacao.data,
    'pilar__nome': apreciacao.pilar.nome,
    'feedback__descritivo': apreciacao.feedback.descritivo, 
    'reconhecedor__id': apreciacao.reconhecedor.id,
    'reconhecedor__nome': apreciacao.reconhecedor.nome_abreviado,
    'reconhecido__id': apreciacao.reconhecido.id,
    'reconhecido__nome': apreciacao.reconhecido.nome_abreviado,
    'agradecimentos': obter_agradecimentos(apreciacao, apreciacao.reconhecido.id, apreciacao.reconhecedor.id)
  }, Reconhecimento.objects.filter(reconhecedor = requisicao.user.id).order_by('-id'))

  apreciacoes = {
    'feitas': list(apreciacoes_feitas),
    'recebidas': list(apreciacoes_recebidas)
  }

  return JsonResponse(apreciacoes)

def obter_agradecimentos(apreciacao, id_reconhecido, id_reconhecedor):
  agradecimentos = Agradecimento.objects.filter(reconhecimento = apreciacao.id)
  agradecimento_reconhecido = mapear_agradecimento(agradecimentos.filter(colaborador = id_reconhecido))
  agradecimento_reconhecedor = mapear_agradecimento(agradecimentos.filter(colaborador = id_reconhecedor))

  agradecimentos_mapeados = {
    'agradecimento_reconhecido': list(agradecimento_reconhecido) if agradecimento_reconhecido else None, 
    'agradecimento_reconhecedor': list(agradecimento_reconhecedor) if agradecimento_reconhecedor else None 
  }
  
  return agradecimentos_mapeados

def mapear_agradecimento(agradecimentos):
  return map(lambda agradecimento: {
      'id': agradecimento.id,
      'data': agradecimento.data,
      'mensagem': agradecimento.mensagem,
      'nome_colaborador': Colaborador.objects.get(id=agradecimento.colaborador.id).nome_abreviado,
      'id_colaborador': Colaborador.objects.get(id=agradecimento.colaborador.id).id
  }, agradecimentos)

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

@has_role_decorator('administrador')
def definir_ciclo(requisicao):
  nome_ciclo = requisicao.POST["nome_ciclo"]
  data_inicial = requisicao.POST["data_inicial"]
  data_final = requisicao.POST["data_final"]
  id_usuario_que_modificou = requisicao.POST["usuario_que_modificou"]
  usuario_que_modificou = Colaborador.objects.get(id=id_usuario_que_modificou)
 
  ciclo = Ciclo(nome=nome_ciclo, data_inicial=data_inicial, data_final= data_final)
  ciclo.save()
  
  log_Ciclo = LOG_Ciclo.adicionar(ciclo, usuario_que_modificou, 'Criação do ciclo', nome_ciclo , data_final)
  log_Ciclo.save()

  return JsonResponse({})

@has_role_decorator('administrador')
def alterar_ciclo(requisicao):
  ciclo_futuro = obter_ciclo_futuro()
  id_ciclo = requisicao.POST["id_ciclo"]
  data_final = requisicao.POST["data_final"]
  id_usuario_que_modificou = requisicao.POST["usuario_que_modificou"]
  novo_nome_ciclo = requisicao.POST["novo_nome_ciclo"]
  descricao_da_alteracao = requisicao.POST["descricao_da_alteracao"]
  ciclo = Ciclo.objects.get(id = id_ciclo)
  usuario_que_modificou = Colaborador.objects.get(id=id_usuario_que_modificou)

  log_Ciclo = LOG_Ciclo.adicionar(ciclo, usuario_que_modificou, descricao_da_alteracao, novo_nome_ciclo, data_final)
  log_Ciclo.save()

  data_final_em_date_time = datetime.strptime(data_final, '%Y-%m-%d').date()
  ciclo.alterar_ciclo(data_final_em_date_time, novo_nome_ciclo)
  ciclo.save()
  
  if ciclo_futuro and ciclo_futuro.id != int(id_ciclo):
    alterar_data_inicial_ciclo_futuro(ciclo_futuro, data_final_em_date_time, usuario_que_modificou)

  return JsonResponse({})
  
def  alterar_data_inicial_ciclo_futuro(ciclo_futuro, data_final_em_date_time, usuario_que_modificou):
  if ciclo_futuro != None:
    nova_data_inicial = data_final_em_date_time + timedelta(days=1)
    if ciclo_futuro.data_final != None and ciclo_futuro.data_final <= nova_data_inicial:
      data_final = None
    else:
      data_final = ciclo_futuro.data_final
    
    log_Ciclo = LOG_Ciclo.adicionar(ciclo_futuro, usuario_que_modificou, "Alteração da data inicial devido a mudança da data final do ciclo atual", ciclo_futuro.nome, data_final)
    log_Ciclo.save()
    
    ciclo_futuro.alterar_data_inicial_ciclo(nova_data_inicial)
    ciclo_futuro.save()
    

@has_role_decorator('administrador')
def obter_informacoes_ciclo_atual(requisicao):
  ciclo = obter_ciclo_atual()
  log = LOG_Ciclo.objects.filter(ciclo=ciclo).order_by('-data_da_modificacao').first()
  if log.usuario_que_modificou != None:
    colaborador = Colaborador.objects.get(id=log.usuario_que_modificou.id)
  else:
    colaborador = "Automático"

  if ciclo.data_final == None:
    data_final = ""
    data_final_formatada = ""
    porcentagem = "0"
  else:
    data_final = ciclo.data_final
    data_final_formatada = data_final.strftime('%d/%m/%Y')
    porcentagem = ciclo.calcular_porcentagem_progresso()

  resposta = {
    'id_ciclo': ciclo.id,
    'nome_do_ciclo': ciclo.nome,
    'data_inicial': ciclo.data_inicial,
    'data_inicial_formatada': ciclo.data_inicial.strftime('%d/%m/%Y'),
    'data_final': data_final,
    'data_final_formatada': data_final_formatada,
    'nome_usuario_que_modificou': colaborador.nome_abreviado if(colaborador != "Automático") else "Automático",
    'descricao_da_alteracao': log.descricao_da_alteracao,
    'data_ultima_alteracao': log.data_da_modificacao.strftime('%d/%m/%Y'),
    'porcentagem_do_progresso': porcentagem
  }
  
  return JsonResponse(resposta)

@has_role_decorator('administrador')
def obter_informacoes_ciclo_futuro(requisicao):
  if (obter_ciclo_atual().data_final) != None:
    ciclo_futuro_obtido = obter_ciclo_futuro()
    data_final_ciclo_atual = obter_ciclo_atual().data_final
    data_inicio_previsto_ciclo_futuro =  data_final_ciclo_atual + timedelta(days=1)
    data_inicio_previsto_ciclo_futuro_formatada = data_inicio_previsto_ciclo_futuro.strftime('%d/%m/%Y')
  else:
    ciclo_futuro_obtido = None
    data_final_ciclo_atual = None
    data_inicio_previsto_ciclo_futuro = None
    data_inicio_previsto_ciclo_futuro_formatada = None


  if ciclo_futuro_obtido != None:
    log = LOG_Ciclo.objects.filter(ciclo=ciclo_futuro_obtido).order_by('-data_da_modificacao').first()
    if log.usuario_que_modificou != None:
      colaborador = Colaborador.objects.get(id=log.usuario_que_modificou.id)
    else:
      colaborador = "Automático"
    
    if ciclo_futuro_obtido.data_final != None:
      data_final = ciclo_futuro_obtido.data_final
      data_final_formatada = data_final.strftime('%d/%m/%Y')
      
    else :
      data_final = ""
      data_final_formatada = ""

    ciclo_futuro = {
      'id_ciclo': ciclo_futuro_obtido.id,
      'nome_do_ciclo': ciclo_futuro_obtido.nome,
      'data_inicial': ciclo_futuro_obtido.data_inicial,
      'data_inicial_formatada': ciclo_futuro_obtido.data_inicial.strftime('%d/%m/%Y'),
      'data_final': data_final,
      'data_final_formatada': data_final_formatada,
      'nome_usuario_que_modificou': colaborador.nome_abreviado if(colaborador != "Automático") else "Automático",
      'tempo_restante_de_dias' : ciclo_futuro_obtido.calcularDiasParaIniciarCiclo().days,
    }
  else:
    ciclo_futuro = None
    
  resposta = {
    'ciclo_futuro': ciclo_futuro,
    'previsao_data'  : {
      'data_prevista_para_inicio': data_inicio_previsto_ciclo_futuro,
      'data_prevista_para_inicio_formatada': data_inicio_previsto_ciclo_futuro_formatada,
    },
    'data_final_ciclo_atual': data_final_ciclo_atual,
  }

  return JsonResponse(resposta)


@has_role_decorator('administrador')
def ciclos_passados(requisicao):
  ciclos_passados_obtidos = obter_ciclos_passados().order_by('-id')
  
  if ciclos_passados_obtidos != None:
    ciclos_passados = map(lambda ciclo: { 
      'id_ciclo': ciclo.id, 
      'nome': ciclo.nome, 
      'nome_autor': obter_nome_usuario_que_modificou(ciclo), 
      'data_inicial': ciclo.data_inicial.strftime('%d/%m/%Y'), 
      'data_final': ciclo.data_final.strftime('%d/%m/%Y') 
      }, ciclos_passados_obtidos)

    lista_todos_ciclos_passados = list(ciclos_passados)

    paginator = Paginator(lista_todos_ciclos_passados, 2)

    secoes = []

    for i in range(1, paginator.num_pages + 1):
      secao = {
        'id_secao': i,
        'ciclos': []
      }

      secao["ciclos"] = paginator.page(i).object_list
      secoes.append(secao)
  
  else:
    secoes = None
    
  resposta = {
    'secoes': secoes
  }	
  
  return JsonResponse(resposta, safe=False)

@has_role_decorator('administrador')
def historico_alteracoes(requisicao):
  historico_alteracoes = map(lambda LOG_Ciclo: { 
    'antigo_nome_do_ciclo': LOG_Ciclo.antigo_nome_ciclo, 
    'nome_autor': LOG_Ciclo.usuario_que_modificou.nome_abreviado if(LOG_Ciclo.usuario_que_modificou != None) else "Automático", 
    'data_anterior': LOG_Ciclo.antiga_data_final.strftime('%d/%m/%Y') if(LOG_Ciclo.antiga_data_final != None) else "", 
    'nova_data': LOG_Ciclo.nova_data_alterada.strftime('%d/%m/%Y') if (LOG_Ciclo.nova_data_alterada != None) else "", 
    'data_alteracao': LOG_Ciclo.data_da_modificacao.strftime('%d/%m/%Y'), 
    'motivo_alteracao': LOG_Ciclo.descricao_da_alteracao, 
    'novo_nome_ciclo' : LOG_Ciclo.novo_nome_ciclo
  }, obter_historico_de_alteracoes().order_by('-id'))

  paginator = Paginator(list(historico_alteracoes), 2)

  secoes = []

  for i in range(1, paginator.num_pages + 1):
    secao = {
      'id_secao': i,
      'LOG_ciclos': []
    }

    secao["LOG_ciclos"] = paginator.page(i).object_list
    secoes.append(secao)
      
  resposta = {
    'secoes': secoes
  }	
  
  return JsonResponse(resposta, safe=False)

def obter_ciclo_atual():
  try:
    return Ciclo.objects.get(data_final__gte=date.today(), data_inicial__lte=date.today())
  except Ciclo.DoesNotExist:
    return Ciclo.objects.get(data_final__isnull=True, data_inicial__lte=date.today())

def obter_ciclo_futuro():
  ciclo_atual = obter_ciclo_atual()
  try:
    if ciclo_atual.data_final != None:
      return Ciclo.objects.get(data_inicial__gt=ciclo_atual.data_final)
    else:
      return None
  except Ciclo.DoesNotExist:
    return None

def obter_ciclos_passados():
  return Ciclo.objects.filter(data_final__lt=date.today())

def obter_nome_usuario_que_modificou(ciclo):
  log = LOG_Ciclo.objects.get(ciclo=ciclo.id)
  colaborador = Colaborador.objects.get(id=log.usuario_que_modificou.id)
  return colaborador.nome_abreviado

def obter_historico_de_alteracoes():
  log = LOG_Ciclo.objects.all()
  return log

def abreviar_nome(nome):
  return nome.split(' ')[0] + ' ' + nome.split(' ')[-1]

def criar_colaborador(nome, foto):
  return type('',(object,),{
          'nome': abreviar_nome(nome),
          'colaborar_sempre': 0,
          'fazer_diferente': 0,
          'focar_nas_pessoas': 0,
          'planejar_entregar_aprender': 0,
          'todos_reconhecimentos': 0,
          'reconhecimentos_feitos': 0,
          'foto': foto
        })()

def verificar_pilar_colaborador(colaborador, colaborador_transformado):
  id_pilar = colaborador[1]
  quantidade = colaborador[0]
  if id_pilar == 1:
    colaborador_transformado.colaborar_sempre = quantidade
  elif id_pilar == 2:
    colaborador_transformado.fazer_diferente = quantidade
  elif id_pilar == 3:
    colaborador_transformado.focar_nas_pessoas = quantidade
  elif id_pilar == 4:
    colaborador_transformado.planejar_entregar_aprender = quantidade
  
  colaborador_transformado.todos_reconhecimentos += quantidade
  
  return colaborador_transformado

@has_role_decorator('administrador')
def ranking_por_periodo(requisicao):
    data_inicio = requisicao.POST['data_inicio']
    data_fim = requisicao.POST['data_fim']
    
    colaboradores_apreciacoes_recebidas = obter_ranking_de_apreciacoes_recebidas(data_inicio, data_fim)
    colaboradores_apreciacoes_feitas = obter_ranking_de_apreciacoes_feitas(data_inicio, data_fim)
    
    if colaboradores_apreciacoes_recebidas == None and colaboradores_apreciacoes_feitas == None:
      return JsonResponse(status=403, data={'mensagem': 'Não foram encontrados registros para esta data!'})
      
    colaboradores_transformados = []
    colaborador_transformado = None
    for colaborador in colaboradores_apreciacoes_recebidas:      
      if colaborador_transformado == None or colaborador_transformado.nome != colaborador[2]:
        if colaborador_transformado != None:
          colaboradores_transformados.append(colaborador_transformado)
        colaborador_transformado = criar_colaborador(colaborador[2], colaborador[4])
        verificar_pilar_colaborador(colaborador, colaborador_transformado)
      else:
        verificar_pilar_colaborador(colaborador, colaborador_transformado)
      
    if colaborador_transformado != None:
      colaboradores_transformados.append(colaborador_transformado)

    for colaborador in colaboradores_apreciacoes_feitas:
      colaborador_retornado = busca_colaborador_ranking(colaborador, colaboradores_transformados)
      if colaborador_retornado != None:
        colaborador_retornado.reconhecimentos_feitos = colaborador[0]
      else:
        novo_colaborador = criar_colaborador(colaborador[2], colaborador[3])
        novo_colaborador.reconhecimentos_feitos = colaborador[0]
        colaboradores_transformados.append(novo_colaborador)

    if len(colaboradores_transformados) != 0:
      colaboradores_ordenados = sorted(colaboradores_transformados, key=lambda x: x.todos_reconhecimentos, reverse=True)
      transformacao = lambda colaborador : { 
        'nome' : colaborador.nome,
        'todos_reconhecimentos' : colaborador.todos_reconhecimentos,
        'colaborar_sempre': colaborador.colaborar_sempre,
        'focar_nas_pessoas': colaborador.focar_nas_pessoas,
        'fazer_diferente': colaborador.fazer_diferente,
        'planejar_entregar_aprender': colaborador.planejar_entregar_aprender,
        'reconhecimentos_feitos' : colaborador.reconhecimentos_feitos,
        'foto': colaborador.foto
      }
      
      colaboradores = map(transformacao, colaboradores_ordenados)
    else:
      colaboradores = ""

    return JsonResponse({'colaboradores': list(colaboradores)})

def busca_colaborador_ranking(colaborador, colaboradores_transformados):
  for colaborador_transformado in colaboradores_transformados:
    if colaborador[2] == colaborador_transformado.nome:
      return colaborador_transformado
  return None

def obter_ranking_de_apreciacoes_recebidas(data_inicial, data_final):
  with connection.cursor() as cursor:
    cursor.execute('''
    SELECT count(*), r.pilar_id, l.nome, r.reconhecido_id, l.foto
    FROM public."Reconhecimentos_reconhecimento" r
    JOIN public."Login_colaborador" l ON r.reconhecido_id = l.id
    WHERE r.data BETWEEN %s AND %s
    GROUP by l.nome, r.pilar_id, r.reconhecido_id, l.foto
    ORDER by l.nome, r.reconhecido_id, r.pilar_id
    ''', [data_inicial, data_final])
    
    ranking_de_apreciacoes_recebidas = cursor.fetchall()
  return ranking_de_apreciacoes_recebidas

def obter_ranking_de_apreciacoes_feitas(data_inicial, data_final):
  with connection.cursor() as cursor:
    cursor.execute('''
    SELECT count(*), r.reconhecedor_id, l.nome, l.foto
    FROM public."Reconhecimentos_reconhecimento" r
    JOIN public."Login_colaborador" l ON r.reconhecedor_id = l.id
    WHERE r.data BETWEEN %s AND %s
    GROUP by r.reconhecedor_id, l.nome, l.foto
    ORDER by l.nome, r.reconhecedor_id
    ''', [data_inicial, data_final])
    ranking_de_apreciacoes_feitas = cursor.fetchall()
  return ranking_de_apreciacoes_feitas
  
def converterData(data):
  return datetime.strptime(data, "%Y-%m-%d").date()

@has_role_decorator('administrador')
def obter_notificacoes_do_administrador(requisicao):
  notificacao = AprecieConfig.obter_mensagem_notificacao()

  data = {
    'mensagem': notificacao
  }

  return JsonResponse(data)