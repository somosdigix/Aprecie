from django.db import models

class Valor(models.Model):
	nome = models.CharField(max_length=200, blank=False)

class Reconhecimento(models.Model):
	funcionario = models.ForeignKey('Login.Funcionario', blank=False)
	valor = models.ForeignKey(Valor, blank=False)
	justificativa = models.CharField(max_length=200, blank=False)