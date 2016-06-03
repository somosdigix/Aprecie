from Aprecie.base import ExcecaoDeDominio
from django.db import models
import django
from datetime import date

class DescricaoDoValor(models.Model):
 	descricao = models.CharField(max_length=100)

class Valor(models.Model):
	nome = models.CharField(max_length=200)
	resumo = models.CharField(max_length=100)
	descricoes = models.ManyToManyField(DescricaoDoValor)

	@property
	def frases_de_descricao(self):
		return list(self.descricoes.values_list('descricao', flat=True))

class Reconhecimento(models.Model):
	reconhecedor = models.ForeignKey('Login.Colaborador', related_name='reconhecedor')
	reconhecido = models.ForeignKey('Login.Colaborador', related_name='reconhecido')
	valor = models.ForeignKey(Valor)
	justificativa = models.CharField(max_length=1000)
	data = models.DateField(auto_now_add=True)

	def alterar_justificativa(self, nova_justificativa, reconhecedor):
		if self.reconhecedor != reconhecedor:
			raise ExcecaoDeDominio('O reconhecimento só pode ser alterado por quem o elaborou')
		elif self.data != date.today():
			raise ExcecaoDeDominio('O reconhecimento só pode ser alterado no mesmo dia de sua realização')

		self.justificativa = nova_justificativa
