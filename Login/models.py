from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import IntegerField
from bradocs4py import ValidadorCpf

from Aprecie.base import ExcecaoDeDominio


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
	usuario_id_do_chat = models.CharField(max_length=100, null=True)
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

		self.foto = nova_foto_em_base64

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
		

