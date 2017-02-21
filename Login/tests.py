import json
from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from Aprecie.base import ExcecaoDeDominio
from Login.factories import ColaboradorFactory
from Reconhecimentos.models import Reconhecimento, Pilar, Feedback
from Reconhecimentos.factories import ReconhecimentoFactory, FeedbackFactory

class TesteDeColaborador(TestCase):
	def setUp(self):
		self.colaborador = ColaboradorFactory()
		self.reconhecedor = ColaboradorFactory()
		
		self.pilar = Pilar.objects.get(nome='Colaborar sempre')
		self.feedback = FeedbackFactory()

	def testa_que_a_foto_do_colaborador_eh_alterada(self):
		nova_foto = 'base64=???'
		dados_da_requisicao = {
			'nova_foto': nova_foto,
			'id_do_colaborador': self.colaborador.id
		}

		resposta = self.client.post(reverse('alterar_foto'), dados_da_requisicao)

		self.colaborador.refresh_from_db()
		self.assertEqual(nova_foto, self.colaborador.foto)

	def testa_que_deve_retornar_a_lista_de_colaboradores_ja_com_nome_abreviado(self):
		resposta = self.client.get(reverse('obter_colaboradores'))

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual('Alberto Roberto', resposta_json['colaboradores'][0]['nome'])

	def testa_que_a_foto_deve_ser_alterada(self):
		nova_foto = 'base64=????'

		self.colaborador.alterar_foto(nova_foto)

		self.assertEqual(nova_foto, self.colaborador.foto)

	def testa_que_nao_deve_trocar_para_uma_foto_inexistente(self):
		with self.assertRaises(ExcecaoDeDominio) as contexto:
			self.colaborador.alterar_foto(' ')

		self.assertEqual('Foto deve ser informada', contexto.exception.args[0])

	def testa_que_deve_exibir_somente_o_primeiro_nome(self):
		self.assertEqual('Alberto', self.colaborador.primeiro_nome)

	def testa_que_deve_abreviar_o_nome_da_pessoa(self):
		self.assertEqual('Alberto Roberto', self.colaborador.nome_abreviado)

	def testa_que_o_colaborador_nao_pode_reconhecer_sem_informar_seu_feedback(self):
		with self.assertRaises(Exception) as contexto:
			self.colaborador.reconhecer(self.reconhecedor, self.pilar, None)

		self.assertEqual('Feedback deve ser informado', contexto.exception.args[0])

	def testa_o_reconhecimento_de_uma_habilidade(self):
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)
		reconhecimento = self.colaborador.reconhecimentos()[0]

		self.assertEqual(1, len(self.colaborador.reconhecimentos_por_pilar(self.pilar)))
		self.assertEqual(self.reconhecedor, reconhecimento.reconhecedor)
		self.assertEqual(self.pilar, reconhecimento.pilar)

	def testa_que_feedback_esta_no_formato_sci(self):
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)
		reconhecimento = self.colaborador.reconhecimentos()[0]

		self.assertEqual(self.feedback.situacao, reconhecimento.feedback.situacao)
		self.assertEqual(self.feedback.comportamento, reconhecimento.feedback.comportamento)
		self.assertEqual(self.feedback.impacto, reconhecimento.feedback.impacto)

	def testa_que_armazena_a_data_do_reconhecimento(self):
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)
		reconhecimento = self.colaborador.reconhecimentos()[0]

		agora = timezone.now()
		self.assertEqual(agora.year, reconhecimento.data.year)
		self.assertEqual(agora.month, reconhecimento.data.month)
		self.assertEqual(agora.day, reconhecimento.data.day)

	def testa_a_listagem_de_reconhecimentos(self):
		segundoFeedback = FeedbackFactory(situacao = 'Situação 2')

		self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, segundoFeedback)

		pilares_esperados = [ self.pilar, self.pilar ]
		pilar_reconhecidos = map(lambda reconhecimento: reconhecimento.pilar, self.colaborador.reconhecimentos())
		self.assertEqual(pilares_esperados, list(pilar_reconhecidos))

	def testa_a_listagem_de_reconhecimentos_por_pilar(self):
		outroPilar = Pilar.objects.get(nome='Fazer diferente')
		segundoFeedback = FeedbackFactory(situacao = 'Situação 2')
		terceiroFeedback = FeedbackFactory(situacao = 'Situação 3')

		self.colaborador.reconhecer(self.reconhecedor, outroPilar, self.feedback)
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, segundoFeedback)
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, terceiroFeedback)

		self.assertEqual(1, len(self.colaborador.reconhecimentos_por_pilar(outroPilar)))
		self.assertEqual(2, len(self.colaborador.reconhecimentos_por_pilar(self.pilar)))

	def testa_que_o_colaborador_nao_pode_se_reconher(self):
		with self.assertRaises(Exception) as contexto:
			self.colaborador.reconhecer(self.colaborador, self.pilar, self.feedback)

		self.assertEqual('O colaborador nao pode reconher a si próprio', contexto.exception.args[0])

	def testa_que_o_colaborador_nao_pode_receber_um_reconhecimento_duplicado(self):
		self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)

		with self.assertRaises(Exception) as contexto:
			self.colaborador.reconhecer(self.reconhecedor, self.pilar, self.feedback)

		self.assertEqual('Não é possível reconhecer uma pessoa duas vezes pelos mesmos motivos', contexto.exception.args[0])

class TesteDeAutenticacao(TestCase):
	def testa_autenticacao_de_colaborador_existente(self):
		colaborador = ColaboradorFactory()
		dados_da_requisicao = dict(cpf=colaborador.cpf, data_de_nascimento=colaborador.data_de_nascimento.strftime('%d/%m/%Y'))

		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)

		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(colaborador.id, resposta_json['id_do_colaborador'])
		self.assertEqual(colaborador.primeiro_nome, resposta_json['nome_do_colaborador'])

	def testa_autenticacao_de_colaborador_inexistente(self):
		cpf = 'um cpf qualquer'
		data_de_nascimento = '02/01/3001'
		dados_da_requisicao = dict(cpf=cpf, data_de_nascimento=data_de_nascimento)

		resposta = self.client.post(reverse('entrar'), dados_da_requisicao)
		
		resposta_json = json.loads(resposta.content.decode())
		self.assertEqual(403, resposta.status_code)
		self.assertEqual('Oi! Seus dados não foram encontrados. Confira e tente novamente. :)', resposta_json['mensagem'])
