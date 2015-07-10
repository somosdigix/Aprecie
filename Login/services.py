# -*- coding: utf-8 -*-
from Login.models import Funcionario

class ServicoDeAutenticacao():

	def autenticar(self, cpf, data_de_nascimento):
		if not Funcionario.objects.filter(cpf=cpf, data_de_nascimento=data_de_nascimento).exists():
			raise Exception('Colaborador não encontrado, confirme seus dados e tente novamente')

		return Funcionario.objects.get(cpf=cpf, data_de_nascimento=data_de_nascimento)
