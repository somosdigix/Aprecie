import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from Login.factories import ColaboradorFactory
from Reconhecimentos.factories import ReconhecimentoFactory, FeedbackFactory
from Reconhecimentos.models import Valor, Reconhecimento

class TesteDeApiDeReconhecimento(TestCase):
	def logar(self, colaborador):
		dados_da_requisicao = dict(cpf=colaborador.cpf, data_de_nascimento=colaborador.data_de_nascimento.strftime('%d/%m/%Y'))
		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)

	def setUp(self):
		self.reconhecido = ColaboradorFactory()
		self.reconhecedor = ColaboradorFactory()
		self.feedback = FeedbackFactory()
		self.valor = Valor.objects.get(nome='Alegria')

		self.logar(self.reconhecedor)

		self.dados_do_reconhecimento = {
			'id_do_reconhecido': self.reconhecido.id,
			'id_do_reconhecedor': self.reconhecedor.id,
			'id_do_valor': self.valor.id,
			'situacao': self.feedback.situacao,
			'comportamento': self.feedback.comportamento,
			'impacto': self.feedback.impacto,
		}

	def testa_o_reconhecimento_de_um_valor_de_um_colaborador(self):
		resposta = self.client.post(reverse('reconhecer'), self.dados_do_reconhecimento)
		ultimo_reconhecimento = self.mapear_reconhecimentos(Reconhecimento.objects.all())[0]

		self.assertEqual(200, resposta.status_code)
		self.assertEqual(self.dados_do_reconhecimento, ultimo_reconhecimento)

	def testa_a_listagem_dos_ultimos_reconhecimentos_realizados(self):
		self.criar_reconhecimentos(2)

		resposta = self.client.post(reverse('ultimos_reconhecimentos'))

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(200, resposta.status_code)
		self.assertEqual(2, len(resposta_json))

	def testa_que_apenas_10_reconhecimentos_sao_listados(self):
		self.criar_reconhecimentos(15)

		resposta = self.client.post(reverse('ultimos_reconhecimentos'))

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(200, resposta.status_code)
		self.assertEqual(10, len(resposta_json))

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
		self.assertEqual(self.valor.id, reconhecedores[0]['valor__id'])
		self.assertEqual(1, reconhecedores[0]['quantidade_de_reconhecimentos'])
		self.assertEqual(reconhecedor2.primeiro_nome, reconhecedores[1]['reconhecedor__nome'])
		self.assertEqual(self.valor.id, reconhecedores[1]['valor__id'])
		self.assertEqual(2, reconhecedores[1]['quantidade_de_reconhecimentos'])

	def mapear_reconhecimentos(self, reconhecimentos):
		return list(map(lambda reconhecimento: {
			'id_do_reconhecido': reconhecimento.reconhecido.id,
			'id_do_reconhecedor': reconhecimento.reconhecedor.id,
			'id_do_valor': reconhecimento.valor.id,
			'situacao': reconhecimento.feedback.situacao,
			'comportamento': reconhecimento.feedback.comportamento,
			'impacto': reconhecimento.feedback.impacto,
		}, reconhecimentos))

	def criar_reconhecimentos(self, quantidade):
		for num in range(0, quantidade):
			self.client.post(reverse('reconhecer'), self.dados_do_reconhecimento)