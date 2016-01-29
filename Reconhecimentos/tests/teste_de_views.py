from django.test import TestCase
from django.core.urlresolvers import reverse
from Login.factories import ColaboradorFactory
from Reconhecimentos.factories import ReconhecimentoFactory
from Reconhecimentos.statics import ValoresDaDigithoBrasil
import json

class TesteDeApiDeReconhecimento(TestCase):

	def logar(self, colaborador):
		dados_da_requisicao = dict(cpf=colaborador.cpf, data_de_nascimento=colaborador.data_de_nascimento.strftime('%d/%m/%Y'))
		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)

	def setUp(self):
		self.reconhecido = ColaboradorFactory()
		self.reconhecedor = ColaboradorFactory()
		self.valor = ValoresDaDigithoBrasil.inquietude
		self.justificativa = 'Você é legal'

		self.logar(self.reconhecedor)

		self.dados_do_reconhecimento = {
			'id_do_reconhecido': self.reconhecido.id,
			'id_do_reconhecedor': self.reconhecedor.id,
			'id_do_valor': self.valor.id,
			'justificativa': self.justificativa
		}

	def testa_o_reconhecimento_de_um_valor_de_um_colaborador(self):
		resposta = self.client.post(reverse('reconhecer'), self.dados_do_reconhecimento)

		self.assertEqual(200, resposta.status_code)
		self.assertEqual(1, len(self.reconhecido.reconhecimentos_por_valor(self.valor)))

	def testa_a_listagem_dos_ultimos_reconhecimentos_realizados(self):
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
		self.assertEqual(self.reconhecido.id, resposta_json[0]['id_do_reconhecido'])
		self.assertEqual(self.reconhecido.nome_abreviado, resposta_json[0]['nome_do_reconhecido'])
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

	def testa_reconhecimentos_de_uma_pessoa_agrupados_por_reconhecedor(self):
		reconhecido = ColaboradorFactory()
		reconhecedor1 = ColaboradorFactory()
		reconhecedor2 = ColaboradorFactory()
		reconhecimento1 = ReconhecimentoFactory(reconhecedor=reconhecedor1, reconhecido=reconhecido)
		reconhecimento2 = ReconhecimentoFactory(reconhecedor=reconhecedor2, reconhecido=reconhecido)
		reconhecimento3 = ReconhecimentoFactory(reconhecedor=reconhecedor2, reconhecido=reconhecido)

		resposta = self.client.get(reverse('reconhecimentos_por_reconhecedor', args=[reconhecido.id]))

		resultado = json.loads(resposta.content.decode())
		reconhecedores = resultado.get('reconhecedores')
		self.assertEqual(2, len(reconhecedores))

		self.assertEqual(reconhecedor1.primeiro_nome, reconhecedores[0]['reconhecedor__nome'])
		self.assertEqual(ValoresDaDigithoBrasil.inquietude.id, reconhecedores[0]['valor__id'])
		self.assertEqual(1, reconhecedores[0]['quantidade_de_reconhecimentos'])
		self.assertEqual(reconhecedor2.primeiro_nome, reconhecedores[1]['reconhecedor__nome'])
		self.assertEqual(ValoresDaDigithoBrasil.inquietude.id, reconhecedores[1]['valor__id'])
		self.assertEqual(2, reconhecedores[1]['quantidade_de_reconhecimentos'])