import json
from Aprecie.base import ExcecaoDeDominio
from datetime import datetime
from Login.models import Colaborador
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from io import BytesIO
import base64
from PIL import Image
import os
from django.conf import settings
import re
from Aprecie.base import acesso_anonimo, acesso_exclusivo_com_token
from Login.services import ServicoDeInclusaoDeColaboradores

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

  return JsonResponse(status=200, data={
    'id_do_colaborador': colaborador_autenticado.id,
    'nome_do_colaborador': colaborador_autenticado.primeiro_nome,
  })

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

@acesso_exclusivo_com_token
def inserir_colaboradores(requisicao):
	colaboradores = json.loads(requisicao.body)['colaboradores']

	retorno_da_inclusao = \
		ServicoDeInclusaoDeColaboradores().incluir(colaboradores)
	
	return JsonResponse(data=retorno_da_inclusao, status=200)