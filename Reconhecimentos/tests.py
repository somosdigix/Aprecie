# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from Login.models import Funcionario
from Reconhecimentos.models import Valor
from Reconhecimentos.models import Reconhecimento
from Reconhecimentos.statics import ValoresDaDigithoBrasil
from Reconhecimentos.views import reconhecer

class TesteDeReconhecimento(TestCase):

	def testa_o_reconhecimento_de_uma_habilidade(self):
		funcionario = Funcionario.objects.create(nome='Renan', cpf='00000000000', data_de_nascimento='2000-12-01')
		proatividade = ValoresDaDigithoBrasil.proatividade
		inquietude = ValoresDaDigithoBrasil.inquietude

		funcionario.reconhecer(proatividade, 'Foi legal');
		funcionario.reconhecer(inquietude, 'Voce realmente questiona as coisas');
		funcionario.reconhecer(proatividade, 'Parabens pela iniciativa');

		self.assertEqual(2, funcionario.reconhecimentos(proatividade))

class TesteDeApiDeReconhecimento(TestCase):

	def testa_o_reconhecimento_de_um_valor_de_um_funcionario(self):
		funcionario = Funcionario.objects.create(nome='Renan', cpf='00011122233', data_de_nascimento='2000-12-01')
		valor = Valor.objects.create(nome='Inquietude')

		response = self.client.post(reverse('reconhecer'), { 'cpf': '00011122233', 'idDoValor': valor.id, 'justificativa': 'Você é legal' })

		self.assertEqual(response.status_code, 200)
		self.assertEqual(1, funcionario.reconhecimentos(valor))