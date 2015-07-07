from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from Reconhecimentos.models import Reconhecimento

class Funcionario(models.Model):
	id = models.AutoField(primary_key=True)
	nome = models.CharField(max_length="200", blank=False)
	cpf = models.CharField(max_length="11", unique=True, blank=False)
	data_de_nascimento = models.DateField(blank=False)

	def reconhecer(self, valor, justificativa):
		Reconhecimento.objects.create(funcionario=self, valor=valor, justificativa=justificativa)

	def reconhecimentos(self):
		return Reconhecimento.objects.filter(funcionario=self)

	def reconhecimentos_por_valor(self, valor):
		return self.reconhecimentos().filter(valor=valor)