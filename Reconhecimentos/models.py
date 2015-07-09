from django.db import models

class Valor(models.Model):
	nome = models.CharField(max_length=200)

class Reconhecimento(models.Model):
	funcionario = models.ForeignKey('Login.Funcionario')
	valor = models.ForeignKey(Valor)
	justificativa = models.CharField(max_length=200)