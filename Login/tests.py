from django.test import TestCase
from datetime import datetime
from django.contrib.auth import authenticate
from models import Funcionario

class TesteDeAutenticacao(TestCase):

	def testa_autenticacao_de_funcionario_inexistente(self):
		cpf = "um cpf qualquer"
		data_de_nascimento = datetime.today()

		funcionario = authenticate(cpf=cpf, data_de_nascimento=data_de_nascimento)

		self.assertIsNone(funcionario)

	def testa_autenticacao_de_funcionario_existente(self):
		nome = "Guilherme Barbosa Ferreira"
		data_de_nascimento = datetime(1991, 3, 16)
		cpf = "16457244335"
		funcionario = Funcionario.objects.create(cpf=cpf, data_de_nascimento=data_de_nascimento, nome=nome)

		funcionario_autenticado = authenticate(cpf=cpf, data_de_nascimento=data_de_nascimento)

		self.assertEqual(funcionario, funcionario_autenticado)