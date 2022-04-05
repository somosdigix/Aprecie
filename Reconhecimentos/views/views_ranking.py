from django.http import JsonResponse
from rolepermissions.decorators import has_role_decorator
from django.db import connection

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