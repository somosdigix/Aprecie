# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from Login.models import Funcionario
from Reconhecimentos.models import Valor
from Reconhecimentos.models import Reconhecimento
from Reconhecimentos.statics import ValoresDaDigithoBrasil
from Reconhecimentos.views import reconhecer

class TesteDeReconhecimento(TestCase):

	def setUp(self):
		self.funcionario = Funcionario.objects.create(nome='Renan', cpf='00000000000', data_de_nascimento='2000-12-01')

	def testa_o_reconhecimento_de_uma_habilidade(self):
		inquietude = ValoresDaDigithoBrasil.inquietude
		justificativa = 'Foi legal'

		self.funcionario.reconhecer(inquietude, justificativa);
		reconhecimento = self.funcionario.reconhecimentos()[0]

		self.assertEqual(1, len(self.funcionario.reconhecimentos_por_valor(inquietude)))
		self.assertEqual(inquietude, reconhecimento.valor)
		self.assertEqual(justificativa, reconhecimento.justificativa)

	def testa_a_listagem_de_reconhecimentos(self):
		proatividade = ValoresDaDigithoBrasil.proatividade
		inquietude = ValoresDaDigithoBrasil.inquietude

		self.funcionario.reconhecer(proatividade, 'Foi legal');
		self.funcionario.reconhecer(inquietude, 'Voce realmente questiona as coisas');

		self.assertEqual(2, len(self.funcionario.reconhecimentos()))
		self.assertEqual(proatividade, self.funcionario.reconhecimentos()[0].valor)
		self.assertEqual(inquietude, self.funcionario.reconhecimentos()[1].valor)

	def testa_a_listagem_de_reconhecimentos_por_valor(self):
		proatividade = ValoresDaDigithoBrasil.proatividade
		inquietude = ValoresDaDigithoBrasil.inquietude

		self.funcionario.reconhecer(proatividade, 'Foi legal');
		self.funcionario.reconhecer(inquietude, 'Voce realmente questiona as coisas');
		self.funcionario.reconhecer(proatividade, 'Parabens pela iniciativa');

		self.assertEqual(1, len(self.funcionario.reconhecimentos_por_valor(inquietude)))
		self.assertEqual(2, len(self.funcionario.reconhecimentos_por_valor(proatividade)))

class TesteDeApiDeReconhecimento(TestCase):

	def testa_o_reconhecimento_de_um_valor_de_um_funcionario(self):
		funcionario = Funcionario.objects.create(nome='Renan', cpf='00011122233', data_de_nascimento='2000-12-01')
		inquietude = ValoresDaDigithoBrasil.inquietude

		response = self.client.post(reverse('reconhecer'), { 'cpf': '00011122233', 'valor_id': inquietude.id, 'justificativa': 'Você é legal' })

		self.assertEqual(response.status_code, 200)
		self.assertEqual(1, len(funcionario.reconhecimentos_por_valor(inquietude)))