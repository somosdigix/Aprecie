from django.db import models
from django.utils import timezone

class Valor(models.Model):
	nome = models.CharField(max_length=200)

class Reconhecimento(models.Model):
	reconhecedor = models.ForeignKey('Login.Funcionario', related_name='reconhecedor')
	reconhecido = models.ForeignKey('Login.Funcionario', related_name='reconhecido')
	valor = models.ForeignKey(Valor)
	justificativa = models.CharField(max_length=200)
	data = models.DateTimeField(default=timezone.now())