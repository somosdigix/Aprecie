import json
from datetime import datetime
from Login.models import Colaborador, LOG_Administrador
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from io import BytesIO
import base64
from PIL import Image
import os
from django.conf import settings
import re
from Aprecie.base import acesso_anonimo
from Aprecie import settings
from Login.services import ServicoDeInclusaoDeColaboradores, ServicoDeBuscaDeColaboradores, ServicoDeBuscaDeColaborador, ServicoDeEdicaoDeColaborador
from Reconhecimentos.views import converte_boolean
from rolepermissions.roles import assign_role, remove_role
from rolepermissions.decorators import has_role_decorator
from datetime import date
from rolepermissions.checkers import has_role
import requests



@acesso_anonimo
def entrar(requisicao):
	cpf = requisicao.POST['cpf']
	data_de_nascimento = datetime.strptime(requisicao.POST['data_de_nascimento'], '%d/%m/%Y')

	# TODO: Pensar uma forma melhor do que lançar excecao e extrair daqui
	colaborador_autenticado = authenticate(cpf=cpf, data_de_nascimento=data_de_nascimento)
  
	if colaborador_autenticado:
		login(requisicao, colaborador_autenticado)
	else:
		return JsonResponse(status=403, data={
			'mensagem': 'Oi! Seus dados não foram encontrados. Confira e tente novamente. :)'
		})
	  
	data = {
    'id_do_colaborador': colaborador_autenticado.id,
	  'nome_do_colaborador': colaborador_autenticado.primeiro_nome,
	  'administrador': colaborador_autenticado.administrador,
	  'recursos_humanos': has_role(colaborador_autenticado, 'recursos_humanos')
	}

	return JsonResponse(data, status=200)

def alterar_foto(requisicao):
	id_do_colaborador = requisicao.POST['id_do_colaborador']
	nova_foto = requisicao.POST['nova_foto']

	colaborador = Colaborador.objects.get(pk=id_do_colaborador)
	colaborador.alterar_foto(nova_foto)
	colaborador.save()

	return JsonResponse({})

def obter_imagem(colaborador):
	if colaborador.foto:
		padrao = r'^data:image/.+;base64,(?P<b64>.+)'
		match = re.match(padrao, colaborador.foto)
		b64 = match.group('b64')
		image = Image.open(BytesIO(base64.b64decode(b64)))
	else:
		caminho_da_foto_padrao = os.path.join(settings.STATIC_ROOT, "img", "sem-foto.png")
		image = Image.open(caminho_da_foto_padrao)

	return image

def foto_do_perfil(requisicao, id_do_colaborador):
	# TODO: Tratar outras extensoes de imagem
	eh_miniatura = int(requisicao.GET['eh_miniatura'])
	colaborador = Colaborador.objects.get(pk=id_do_colaborador)

	image = obter_imagem(colaborador)
	extensao = image.format

	if eh_miniatura:
		image.thumbnail((50,50))

	response = HttpResponse(content_type="image/{0}".format(extensao))

	image.save(response, extensao)
	return response

def obter_colaboradores(requisicao):
	colaboradores = Colaborador.objects.all()
	transformacao = lambda colaborador: { 'id': colaborador.id, 'nome': colaborador.nome_abreviado }
	colaboradores = map(transformacao, colaboradores)
	return JsonResponse({ 'colaboradores': list(colaboradores) })

@has_role_decorator('recursos_humanos')
def inserir_colaboradores(requisicao):
	colaboradores = json.loads(requisicao.body)['colaboradores']

	retorno_da_inclusao = \
		ServicoDeInclusaoDeColaboradores().incluir(colaboradores)
	
	return JsonResponse(data=retorno_da_inclusao, status=200)

@has_role_decorator('recursos_humanos')
def editar_colaboradores(requisicao):
	colaborador = requisicao.POST['colaborador']

	retorno_da_inclusao = \
		ServicoDeEdicaoDeColaborador().editar(colaborador)
	
	return JsonResponse(data=retorno_da_inclusao, status=200)

@has_role_decorator('recursos_humanos')
def buscar_colaboradores_para_RH(requisicao, tipo_ordenacao):
	retorno_da_busca = ServicoDeBuscaDeColaboradores().buscar(tipo_ordenacao)
	
	return JsonResponse(data=retorno_da_busca, status=200)

@has_role_decorator('recursos_humanos')
def buscar_colaborador(requisicao, id_colaborador):
	retorno_da_busca = ServicoDeBuscaDeColaborador().buscar(id_colaborador)
	
	return JsonResponse(data=retorno_da_busca, status=200)

def validar_usuario_logado(requisicao):
	id_da_sessao = int(requisicao.POST['id'])
	sessao_administrador = converte_boolean(requisicao.POST['administrador'])
	id = requisicao.user.id
	administrador = requisicao.user.administrador

	if id_da_sessao != id or id_da_sessao == None or sessao_administrador != administrador:
		logout(requisicao)
		return JsonResponse({'valido': False})

	elif id_da_sessao == id and sessao_administrador == administrador:
		return JsonResponse({'valido': True})

@has_role_decorator('administrador')
def switch_administrador(requisicao):
    id_do_colaborador = requisicao.POST['id_do_colaborador']
    eh_administrador  = requisicao.POST['eh_administrador']
    colaborador = Colaborador.objects.get(id = id_do_colaborador)

    administrador = requisicao.user

    eh_administrador = converte_boolean(eh_administrador)
    
    if eh_administrador:
      assign_role(colaborador, 'administrador')
      gerar_log_administrador(administrador, colaborador, "O Administrador: " + administrador.nome_abreviado + " setou o usuario: " + colaborador.nome_abreviado + " como administrador")
      colaborador.tornar_administrador()
      colaborador.save()
    
    else:
      remove_role(colaborador, 'administrador')
      gerar_log_administrador(administrador, colaborador, "O Administrador: " + administrador.nome_abreviado + " retirou os privilegios do usuario: " + colaborador.nome_abreviado)
      colaborador.remover_administrador()
      colaborador.save()

    return JsonResponse({})

def gerar_log_administrador(administrador, colaborador, descricao):
	LOG_Administrador.objects.create(administrador = administrador, colaborador = colaborador, descricao = descricao)

def obter_administradores(requisicao):
  administradores =  map(lambda colaborador: {
    'nome': colaborador.nome_abreviado,
    'foto': colaborador.foto,    
  }, Colaborador.objects.all().filter(administrador=1))

  return JsonResponse({'administradores': list(administradores)})


def obter_logs_administradores(requisicao):
	historico = obtem_historico(requisicao)

	historico_logs = map (lambda log_administrador :{
		'data': log_administrador.data_modificacao.strftime('%d/%m/%Y'),
		'mensagem': log_administrador.descricao
	}, historico)

	return JsonResponse({'historico_logs': list(historico_logs)})

def obtem_historico(requisicao):
	data_inicio = None
	data_fim = None
	
	historico = LOG_Administrador.objects.all()

	
	if 'data_inicio' in requisicao.POST:
		data_inicio = requisicao.POST['data_inicio']
		if data_inicio != None and data_inicio != '':

			historico = historico.filter(data_modificacao__gte= data_inicio)
	
	if 'data_fim' in requisicao.POST:
		data_fim = requisicao.POST['data_fim']
		if data_fim != None and data_fim != '':
			historico = historico.filter(data_modificacao__lte=data_fim)
	
	return historico

def validar_usuario_id_do_chat(requisicao, usuario_id_do_chat):
	url = 'https://discord.com/api/v10/users/' + usuario_id_do_chat
	token = settings.DISCORD_KEY
	headers = {'Authorization': 'Bot ' + token}
	resposta = requests.get(url, headers=headers)
	respostaFormatada = json.loads(resposta.text)
	if resposta.status_code == 200:
		return JsonResponse({'status': 200,'username': respostaFormatada['username']})
	else:
		return JsonResponse({'status': 404, 'message': respostaFormatada['message']})