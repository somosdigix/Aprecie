from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from Reconhecimentos.models import Reconhecimento
from bradocs4py import ValidadorCpf
from io import BytesIO
import base64
from PIL import Image
from Aprecie.base import ExcecaoDeDominio
import re
import os


class CPF():
	def __init__(self, valor='') -> None:
		self.valor = valor.strip().replace('.', '').replace('-', '').replace(' ', '')
		self.eh_valido = ValidadorCpf.validar(valor)

	def __str__(self) -> str:
		return self.valor


class Colaborador(AbstractBaseUser, PermissionsMixin):
	id = models.AutoField(primary_key=True)
	cpf = models.CharField(max_length=11, unique=True)
	nome = models.CharField(max_length=200)
	data_de_nascimento = models.DateField()
	foto = models.TextField(default=None, null=True)
	administrador = models.BooleanField(default=False)
	data_ultimo_reconhecimento = models.DateField(null=True)

	USERNAME_FIELD = 'cpf'

	@property
	def primeiro_nome(self):
		return Colaborador.obter_primeiro_nome(self.nome)

	@property
	def nome_abreviado(self):
		return Colaborador.obter_primeiro_nome(self.nome) + ' ' + Colaborador.obter_ultimo_nome(self.nome)

	@staticmethod
	def obter_primeiro_nome(nome):
		return nome.split(' ')[0]

	@staticmethod
	def obter_ultimo_nome(nome):
		return nome.split(' ')[-1]

	def alterar_foto(self, nova_foto_em_base64):
		if not nova_foto_em_base64.strip():
			raise ExcecaoDeDominio('Foto deve ser informada')

		# converter
		padrao = r'^data:image/.+;base64,(?P<b64>.+)'
		match = re.match(padrao, nova_foto_em_base64)
		b64 = match.group('b64')
		image = Image.open(BytesIO(base64.b64decode(b64)))
			
		rgb_im = image.convert('RGB')
		rgb_im.save('foto.jpg')

		with open("foto.jpg", "rb") as image_file:
			image_comprimida = base64.b64encode(image_file.read())

		teste = "data:image/jpeg;base64," + image_comprimida.decode("utf-8")

		self.foto = teste
		image.close()
		#TO DO apagar arquivo gerado

	def reconhecer(self, reconhecedor, pilar, feedback):
		if reconhecedor == self:
			raise ExcecaoDeDominio('O colaborador nao pode reconher a si próprio')

		if not feedback:
			raise ExcecaoDeDominio('Feedback deve ser informado')

		if self.ja_possui_um_reconhecimento_identico(reconhecedor, feedback, pilar):
			raise ExcecaoDeDominio(
			    'Não é possível reconhecer uma pessoa duas vezes pelos mesmos motivos')

		self.reconhecido.create(reconhecedor = reconhecedor, pilar = pilar, feedback = feedback)

	def ja_possui_um_reconhecimento_identico(self, reconhecedor, feedback, pilar):
		return self.reconhecido.filter(
				reconhecedor=reconhecedor,
				pilar=pilar,
				feedback__descritivo=feedback.descritivo
			).exists()

	def reconhecimentos(self):
		return self.reconhecido.all()

	def contar_todos_reconhecimentos(self):
		return len(self.reconhecimentos())

	def reconhecimentos_por_pilar(self, pilar):
		return self.reconhecido.filter(pilar = pilar).order_by('-data')

	def reconhecimentos_por_data(self, data_inicio, data_fim):
		reconhecimentos = self.reconhecimentos()
		return reconhecimentos.filter(data__gte= data_inicio).filter(data__lte=data_fim)

	def reconhecimentos_por_pilar_ranking(self, pilar, reconhecimentos):
		return reconhecimentos.filter(pilar = pilar).order_by('-data')
		
	def tornar_administrador(self):
		self.administrador = True

	def remover_administrador(self):
		self.administrador = False
		
	def obter_ultima_data_de_publicacao(self):
		return self.data_ultimo_reconhecimento	

	def definir_ultima_data_de_publicacao(self, data):
		self.data_ultimo_reconhecimento = data

	def reconhecimentos_feitos_por_data(self, data_inicio, data_fim):
		reconhecimentos_feitos = Reconhecimento.objects.filter(reconhecedor= self)
		return reconhecimentos_feitos.filter(data__gte= data_inicio).filter(data__lte=data_fim)
 
class LOG_Administrador(models.Model):
	id = models.AutoField(primary_key = True)
	administrador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name="Administrador") 
	colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name="Colaborador")
	data_modificacao = models.DateField(auto_now = True)
	descricao = models.CharField(max_length = 150)