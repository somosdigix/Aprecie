from django.test import TestCase
from django.conf import settings
import http.client
import unittest

class TesteDeFumaca(TestCase):
  None
	# def testa_a_disponibilidade_da_pagina_inicial(self):
	# 	conexao = http.client.HTTPConnection(settings.URL_DO_AMBIENTE)
	# 	conexao.request("GET", "")

	# 	resposta = conexao.getresponse()

	# 	self.assertEqual(200, resposta.status, 
	# 		"{0} não está 200 OK!".format(settings.URL_DO_AMBIENTE))