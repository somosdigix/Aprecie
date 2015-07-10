from django.test import TestCase
from django.conf import settings
import http.client

class TesteDeFumaca(TestCase):

	def testa_a_disponibilidade_da_pagina_inicial(self):
		conexao = http.client.HTTPConnection(settings.URL_DE_PRODUCAO)
		conexao.request("GET", "")
		resposta = conexao.getresponse()

		self.assertEqual(200, resposta.status)