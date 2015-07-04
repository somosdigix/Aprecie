from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from Reconhecimentos.models import Reconhecimento

class Funcionario(AbstractBaseUser):
	id = models.AutoField(primary_key=True)
	nome = models.CharField(max_length="200")
	cpf = models.CharField(max_length="11", unique=True)
	data_de_nascimento = models.DateField()

	REQUIRED_FIELDS = ['nome', 'data_de_nascimento']
	USERNAME_FIELD = 'cpf'

	def reconhecer(self, valor, justificativa):
		Reconhecimento.objects.create(funcionario=self, valor=valor, justificativa=justificativa)

	def reconhecimentos(self, valor):
		return len(Reconhecimento.objects.filter(funcionario=self, valor=valor))