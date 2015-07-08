from django.db import models
from Reconhecimentos.models import Reconhecimento

class Funcionario(models.Model):
	nome = models.CharField(max_length="200", blank=False)
	cpf = models.CharField(max_length="11", unique=True, blank=False)
	data_de_nascimento = models.DateField(blank=False)

	def reconhecer(self, reconhecedor, valor, justificativa):
		#TODO: Permite o reconhecimento de si proprio
		Reconhecimento.objects.create(funcionario=self, valor=valor, justificativa=justificativa)

	def reconhecimentos(self):
		return Reconhecimento.objects.filter(funcionario=self)

	def reconhecimentos_por_valor(self, valor):
		return self.reconhecimentos().filter(valor=valor)