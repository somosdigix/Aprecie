# -*- coding: utf-8 -*-
from django.test import TestCase
from Login.models import Funcionario
from Reconhecimentos.models import Valor
from Reconhecimentos.models import Reconhecimento
from Reconhecimentos.statics import ValoresDaDigithoBrasil
from Reconhecimentos.views import reconhecer
from Login.factories import FuncionarioFactory

class TesteDeReconhecimento(TestCase):

	def setUp(self):
		self.funcionario = FuncionarioFactory.create()

	def testa_o_reconhecimento_de_uma_habilidade(self):
		justificativa = 'Foi legal'

		self.funcionario.reconhecer(ValoresDaDigithoBrasil.inquietude, justificativa);
		reconhecimento = self.funcionario.reconhecimentos()[0]

		self.assertEqual(1, len(self.funcionario.reconhecimentos_por_valor(ValoresDaDigithoBrasil.inquietude)))
		self.assertEqual(ValoresDaDigithoBrasil.inquietude, reconhecimento.valor)
		self.assertEqual(justificativa, reconhecimento.justificativa)

	def testa_a_listagem_de_reconhecimentos(self):
		self.funcionario.reconhecer(ValoresDaDigithoBrasil.responsabilidade, 'Foi legal');
		self.funcionario.reconhecer(ValoresDaDigithoBrasil.inquietude, 'Voce realmente questiona as coisas');

		self.assertEqual(2, len(self.funcionario.reconhecimentos()))
		self.assertEqual(ValoresDaDigithoBrasil.responsabilidade, self.funcionario.reconhecimentos()[0].valor)
		self.assertEqual(ValoresDaDigithoBrasil.inquietude, self.funcionario.reconhecimentos()[1].valor)

	def testa_a_listagem_de_reconhecimentos_por_valor(self):
		self.funcionario.reconhecer(ValoresDaDigithoBrasil.responsabilidade, 'Foi legal');
		self.funcionario.reconhecer(ValoresDaDigithoBrasil.inquietude, 'Voce realmente questiona as coisas');
		self.funcionario.reconhecer(ValoresDaDigithoBrasil.responsabilidade, 'Parabens pela iniciativa');

		self.assertEqual(1, len(self.funcionario.reconhecimentos_por_valor(ValoresDaDigithoBrasil.inquietude)))
		self.assertEqual(2, len(self.funcionario.reconhecimentos_por_valor(ValoresDaDigithoBrasil.responsabilidade)))

