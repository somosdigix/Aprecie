from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Funcionario(AbstractBaseUser):
	nome = models.CharField(max_length="200")
	cpf = models.CharField(max_length="11", primary_key=True)
	data_de_nascimento = models.DateField()

	objects = BaseUserManager()
	REQUIRED_FIELDS = ['nome', 'data_de_nascimento']
	USERNAME_FIELD = 'cpf'
