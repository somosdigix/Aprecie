from django.db import models
from Reconhecimentos.models import Reconhecimento

class Funcionario(models.Model):
	nome = models.CharField(max_length='200')
	cpf = models.CharField(max_length='11', unique=True)
	data_de_nascimento = models.DateField()
	foto = models.TextField(default=None, null=True)

	@property
	def nome_compacto(self):
		nomes = self.nome.split(' ')
		return "{0} {1}".format(nomes[0], nomes[-1])

	def alterar_foto(self, nova_foto_em_base64):
		if not nova_foto_em_base64.strip():
			raise Exception('Foto deve ser informada')
			
		self.foto = nova_foto_em_base64

	def reconhecer(self, reconhecedor, valor, justificativa):
		if reconhecedor == self:
			raise Exception('O colaborador nao pode reconher a si próprio')

		if not justificativa.strip():
			raise Exception('A sua justificativa deve ser informada')

		Reconhecimento.objects.create(reconhecedor=reconhecedor, reconhecido=self, valor=valor, justificativa=justificativa)

	def reconhecimentos(self):
		return Reconhecimento.objects.filter(reconhecido=self)

	def reconhecimentos_por_valor(self, valor):
		return self.reconhecimentos().filter(valor=valor)