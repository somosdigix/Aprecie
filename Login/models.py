from django.db import models
from Aprecie.base import ExcecaoDeDominio
from django.contrib.auth.models import AbstractBaseUser

class Colaborador(AbstractBaseUser):
	cpf = models.CharField(max_length=11, unique=True)
	nome = models.CharField(max_length=200)
	data_de_nascimento = models.DateField()
	foto = models.TextField(default=None, null=True)
	usuario_no_slack = models.CharField(max_length=100, null=True)

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
			
		self.foto = nova_foto_em_base64

	def reconhecer(self, reconhecedor, valor, justificativa):
		if reconhecedor == self:
			raise ExcecaoDeDominio('O colaborador nao pode reconher a si próprio')

		if not justificativa.strip():
			raise ExcecaoDeDominio('A sua justificativa deve ser informada')

		self.reconhecido.create(reconhecedor=reconhecedor, valor=valor, justificativa=justificativa)

	def reconhecimentos(self):
		return self.reconhecido.all()

	def reconhecimentos_por_valor(self, valor):
		return self.reconhecido.filter(valor=valor).order_by('-data')