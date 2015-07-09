from django.test import TestCase
from django.conf import settings
import httplib	

class TesteDeFumaca(TestCase):

	def testa_a_disponibilidade_da_pagina_inicial(self):
		conexao = httplib.HTTPConnection(settings.URL_DE_PRODUCAO)
		conexao.request("GET", "")
		resposta = conexao.getresponse()

		self.assertEqual(200, resposta.status)