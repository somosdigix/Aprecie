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
		funcionario = Funcionario.objects.create(nome='Renan', cpf='00000000000', data_de_nascimento='2000-12-01')

	def testa_o_reconhecimento_de_uma_habilidade(self):
		funcionario = Funcionario.objects.get(cpf='00000000000')
		inquietude = ValoresDaDigithoBrasil.inquietude
		justificativa = 'Foi legal'

		funcionario.reconhecer(inquietude, justificativa);
		reconhecimento = funcionario.reconhecimentos()[0]

		self.assertEqual(1, len(funcionario.reconhecimentos_por_valor(inquietude)))
		self.assertEqual(inquietude, reconhecimento.valor)
		self.assertEqual(justificativa, reconhecimento.justificativa)

	def testa_a_listagem_de_reconhecimentos(self):
		funcionario = Funcionario.objects.get(cpf='00000000000')
		proatividade = ValoresDaDigithoBrasil.proatividade
		inquietude = ValoresDaDigithoBrasil.inquietude

		funcionario.reconhecer(proatividade, 'Foi legal');
		funcionario.reconhecer(inquietude, 'Voce realmente questiona as coisas');

		self.assertEqual(2, len(funcionario.reconhecimentos()))
		self.assertEqual(proatividade, funcionario.reconhecimentos()[0].valor)
		self.assertEqual(inquietude, funcionario.reconhecimentos()[1].valor)

	def testa_a_listagem_de_reconhecimentos_por_valor(self):
		funcionario = Funcionario.objects.get(cpf='00000000000')
		proatividade = ValoresDaDigithoBrasil.proatividade
		inquietude = ValoresDaDigithoBrasil.inquietude

		funcionario.reconhecer(proatividade, 'Foi legal');
		funcionario.reconhecer(inquietude, 'Voce realmente questiona as coisas');
		funcionario.reconhecer(proatividade, 'Parabens pela iniciativa');

		self.assertEqual(1, len(funcionario.reconhecimentos_por_valor(inquietude)))
		self.assertEqual(2, len(funcionario.reconhecimentos_por_valor(proatividade)))

class TesteDeApiDeReconhecimento(TestCase):

	def testa_o_reconhecimento_de_um_valor_de_um_funcionario(self):
		funcionario = Funcionario.objects.create(nome='Renan', cpf='00011122233', data_de_nascimento='2000-12-01')
		inquietude = ValoresDaDigithoBrasil.inquietude

		response = self.client.post(reverse('reconhecer'), { 'cpf': '00011122233', 'valor_id': inquietude.id, 'justificativa': 'Você é legal' })

		self.assertEqual(response.status_code, 200)
		self.assertEqual(1, len(funcionario.reconhecimentos_por_valor(inquietude)))