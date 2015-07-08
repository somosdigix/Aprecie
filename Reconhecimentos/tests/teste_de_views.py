# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from Login.factories import FuncionarioFactory
from Reconhecimentos.statics import ValoresDaDigithoBrasil

class TesteDeApiDeReconhecimento(TestCase):

	def testa_o_reconhecimento_de_um_valor_de_um_funcionario(self):
		reconhecido = FuncionarioFactory()
		reconhecedor = FuncionarioFactory()
		inquietude = ValoresDaDigithoBrasil.inquietude

		response = self.client.post(reverse('reconhecer'), {
			'id_do_reconhecido': reconhecido.id,
			'id_do_reconhecedor': reconhecedor.id,
			'id_do_valor': inquietude.id,
			'justificativa': 'Você é legal' })

		self.assertEqual(response.status_code, 200)
		self.assertEqual(1, len(reconhecido.reconhecimentos_por_valor(inquietude)))