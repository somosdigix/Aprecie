from Aprecie.base import ExcecaoDeDominio
from django.db import models
import django
from datetime import date

class Valor(models.Model):
	nome = models.CharField(max_length=200)

class Reconhecimento(models.Model):
	reconhecedor = models.ForeignKey('Login.Funcionario', related_name='reconhecedor')
	reconhecido = models.ForeignKey('Login.Funcionario', related_name='reconhecido')
	valor = models.ForeignKey(Valor)
	justificativa = models.CharField(max_length=200)
	data = models.DateField(auto_now_add=True)

	def alterar_justificativa(self, nova_justificativa, reconhecedor):
		if self.reconhecedor != reconhecedor:
			raise ExcecaoDeDominio('O reconhecimento só pode ser alterado por quem o elaborou')
		elif self.data != date.today():
			raise ExcecaoDeDominio('O reconhecimento só pode ser alterado no mesmo dia de sua realização')

		self.justificativa = nova_justificativa