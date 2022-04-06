from rolepermissions.decorators import has_role_decorator
from Reconhecimentos.models import Ciclo, LOG_Ciclo
from Login.models import Colaborador
from django.http import JsonResponse
from datetime import date, datetime, timedelta
from django.core.paginator import Paginator

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