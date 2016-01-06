from django.db import models
import django

class Valor(models.Model):
	nome = models.CharField(max_length=200)

class Reconhecimento(models.Model):
	reconhecedor = models.ForeignKey('Login.Funcionario', related_name='reconhecedor')
	reconhecido = models.ForeignKey('Login.Funcionario', related_name='reconhecido')
	valor = models.ForeignKey(Valor)
	justificativa = models.CharField(max_length=200)
	data = models.DateField(auto_now_add=True)