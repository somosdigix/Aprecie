from datetime import datetime
from Login.models import Funcionario
from Login.services import ServicoDeAutenticacao
from django.http import JsonResponse, HttpResponse
from io import StringIO, BytesIO
import base64
from PIL import Image
import os
from django.conf import settings
import re

def entrar(requisicao):
	cpf = requisicao.POST['cpf']
	data_de_nascimento = datetime.strptime(requisicao.POST['data_de_nascimento'], '%d/%m/%Y')

	colaborador_autenticado = ServicoDeAutenticacao().autenticar(cpf, data_de_nascimento)

	return JsonResponse({
		'id_do_colaborador': colaborador_autenticado.id,
		'nome_do_colaborador': colaborador_autenticado.primeiro_nome,
	})

def alterar_foto(requisicao):
	id_do_colaborador = requisicao.POST['id_do_colaborador']
	nova_foto = requisicao.POST['nova_foto']

	colaborador = Funcionario.objects.get(pk=id_do_colaborador)
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
		caminho_da_foto_padrao = os.path.join(settings.STATICFILES_DIRS[0], "img", "sem-foto.png")
		image = Image.open(caminho_da_foto_padrao)

	return image

def foto_do_perfil(requisicao, id_do_colaborador):
	# TODO: Tratar outras extensoes de imagem
	eh_miniatura = int(requisicao.GET['eh_miniatura'])
	colaborador = Funcionario.objects.get(pk=id_do_colaborador)

	image = obter_imagem(colaborador)
	extensao = image.format

	if eh_miniatura:
		image.thumbnail((50,50))

	response = HttpResponse(content_type="image/{0}".format(extensao))

	image.save(response, extensao)
	return response

def obter_funcionarios(requisicao):
	colaboradores = Funcionario.objects.all()
	transformacao = lambda colaborador: { 'id': colaborador.id, 'nome': colaborador.nome_abreviado }
	colaboradores = map(transformacao, colaboradores)
	return JsonResponse({ 'colaboradores': list(colaboradores) })