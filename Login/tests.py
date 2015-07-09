#-*- coding: utf-8 -*-
from django.test import TestCase
from datetime import datetime
from Login.models import Funcionario
from django.core.urlresolvers import reverse
import json

class TesteDeAutenticacao(TestCase):

	def testa_autenticacao_de_funcionario_inexistente(self):
		cpf = "um cpf qualquer"
		data_de_nascimento = '01/01/2001'
		dados_da_requisicao = dict(cpf=cpf, data_de_nascimento=data_de_nascimento)

		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)
		
		resposta_json = json.loads(resposta.content)
		self.assertFalse(resposta_json['autenticado'])
		self.assertEqual(u'Colaborador não encontrado, confirme seus dados e tente novamente', resposta_json['mensagem'])


	def testa_autenticacao_de_funcionario_existente(self):
		nome = "Guilherme Barbosa Ferreira"
		data_de_nascimento = datetime(1991, 3, 16)
		cpf = "16457244335"
		funcionario = Funcionario.objects.create(cpf=cpf, data_de_nascimento=data_de_nascimento, nome=nome)
		dados_da_requisicao = dict(cpf=cpf, data_de_nascimento=data_de_nascimento.strftime("%d/%m/%Y"))

		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)

		resposta_json = json.loads(resposta.content)
		self.assertTrue(resposta_json['autenticado'])
		self.assertEqual(funcionario.id, resposta_json['id_do_colaborador'])
		self.assertEqual(funcionario.nome, resposta_json['nome_do_colaborador'])