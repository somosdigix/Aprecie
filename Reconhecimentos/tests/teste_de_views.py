# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from Login.factories import FuncionarioFactory
from Reconhecimentos.statics import ValoresDaDigithoBrasil


class TesteDeApiDeReconhecimento(TestCase):

	def testa_o_reconhecimento_de_um_valor_de_um_funcionario(self):
		funcionario = FuncionarioFactory()
		inquietude = ValoresDaDigithoBrasil.inquietude

		response = self.client.post(reverse('reconhecer'), { 'cpf': funcionario.cpf, 'valor_id': inquietude.id, 'justificativa': 'Você é legal' })

		self.assertEqual(response.status_code, 200)
		self.assertEqual(1, len(funcionario.reconhecimentos_por_valor(inquietude)))