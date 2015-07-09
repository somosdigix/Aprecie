from django.test import TestCase
from django.conf import settings

class TesteDeFumaca(TestCase):

	def testa_a_disponibilidade_da_pagina_inicial(self):

		resposta = self.client.get(settings.URL_DE_PRODUCAO)

		self.assertEqual(400, resposta.status_code)