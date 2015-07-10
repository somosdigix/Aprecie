# -*- coding: utf-8 -*-
from django.test import TestCase
from datetime import datetime
from Login.models import Funcionario
from Login.services import ServicoDeAutenticacao
from django.core.urlresolvers import reverse
import json

class TesteDoServicoDeAutenticacao(TestCase):

	def testa_a_autenticacao_de_funcionario_existente(self):
		nome = 'Renan Siravegna'
		data_de_nascimento = datetime(1991, 3, 16)
		cpf = '12345678910'
		funcionario = Funcionario.objects.create(cpf=cpf, data_de_nascimento=data_de_nascimento, nome=nome)
		servicoDeAutenticacao = ServicoDeAutenticacao()

		funcionario_autenticado = servicoDeAutenticacao.autenticar(cpf, data_de_nascimento)

		self.assertEqual(funcionario.id, funcionario_autenticado.id)

	def testa_a_autenticacao_de_funcionario_inexistente(self):
		cpf_invalido = '09876543212'
		data_de_nascimento_invalida = datetime(2015, 8, 1)
		servicoDeAutenticacao = ServicoDeAutenticacao()

		with self.assertRaises(Exception) as contexto:
			servicoDeAutenticacao.autenticar(cpf_invalido, data_de_nascimento_invalida)
		
		self.assertEqual('Colaborador não encontrado, confirme seus dados e tente novamente', contexto.exception.message)

class TesteDeAutenticacao(TestCase):

	def testa_autenticacao_de_funcionario_existente(self):
		nome = 'Guilherme Barbosa Ferreira'
		data_de_nascimento = datetime(1991, 3, 16)
		cpf = '16457244335'
		funcionario = Funcionario.objects.create(cpf=cpf, data_de_nascimento=data_de_nascimento, nome=nome)
		dados_da_requisicao = dict(cpf=cpf, data_de_nascimento=data_de_nascimento.strftime('%d/%m/%Y'))

		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)

		resposta_json = json.loads(resposta.content)
		self.assertEqual(funcionario.id, resposta_json['id_do_colaborador'])
		self.assertEqual(funcionario.nome, resposta_json['nome_do_colaborador'])

	def testa_autenticacao_de_funcionario_inexistente(self):
		cpf = 'um cpf qualquer'
		data_de_nascimento = '01/01/2001'
		dados_da_requisicao = dict(cpf=cpf, data_de_nascimento=data_de_nascimento)

		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)
		
		resposta_json = json.loads(resposta.content)
		self.assertEqual(u'Colaborador não encontrado, confirme seus dados e tente novamente', resposta_json['mensagem'])