from django.test import TestCase
from django.core.urlresolvers import reverse
from Login.factories import FuncionarioFactory
from Reconhecimentos.statics import ValoresDaDigithoBrasil
import json

class TesteDeApiDeReconhecimento(TestCase):

	def setUp(self):
		self.reconhecido = FuncionarioFactory()
		self.reconhecedor = FuncionarioFactory()
		self.valor = ValoresDaDigithoBrasil.inquietude
		self.justificativa = 'Você é legal'

		self.dados_do_reconhecimento = {
			'id_do_reconhecido': self.reconhecido.id,
			'id_do_reconhecedor': self.reconhecedor.id,
			'id_do_valor': self.valor.id,
			'justificativa': self.justificativa
		}

	def testa_o_reconhecimento_de_um_valor_de_um_funcionario(self):
		resposta = self.client.post(reverse('reconhecer'), self.dados_do_reconhecimento)

		self.assertEqual(200, resposta.status_code)
		self.assertEqual(1, len(self.reconhecido.reconhecimentos_por_valor(self.valor)))

	def testa_a_listagem_dos_ultimos_reconhecimentos_realzados(self):
		self.criar_reconhecimentos(2)

		resposta = self.client.post(reverse('ultimos_reconhecimentos'))

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(200, resposta.status_code)
		self.assertEqual(2, len(resposta_json))

	def testa_os_detalhes_exibidos_do_ultimo_reconhecimento(self):
		self.criar_reconhecimentos(1)

		resposta = self.client.post(reverse('ultimos_reconhecimentos'))

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(200, resposta.status_code)
		self.assertEqual(self.reconhecido.nome, resposta_json[0]['nome_do_reconhecido'])
		self.assertEqual(self.justificativa, resposta_json[0]['justificativa'])
		self.assertEqual(self.valor.nome, resposta_json[0]['valor'])

	def testa_que_apenas_10_reconhecimentos_sao_listados(self):
		self.criar_reconhecimentos(15)

		resposta = self.client.post(reverse('ultimos_reconhecimentos'))

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(200, resposta.status_code)
		self.assertEqual(10, len(resposta_json))

	def criar_reconhecimentos(self, quantidade):
		for num in range(0, quantidade):
			self.client.post(reverse('reconhecer'), self.dados_do_reconhecimento)