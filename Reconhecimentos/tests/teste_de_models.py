from datetime import date, datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from Aprecie.base import ExcecaoDeDominio
from Login.models import Colaborador
from Login.factories import ColaboradorFactory
from Reconhecimentos.models import Reconhecimento, Valor, Feedback
from Reconhecimentos.views import reconhecer
from Reconhecimentos.factories import ReconhecimentoFactory, ValorFactory, DescricaoDoValorFactory, FeedbackFactory

class TesteDeReconhecimento(TestCase):
	def setUp(self):
		self.feedback = FeedbackFactory()
		self.reconhecido = ColaboradorFactory()
		self.reconhecedor = ColaboradorFactory()
		self.responsabilidade = Valor.objects.get(nome='Responsabilidade')
		self.inquietude = Valor.objects.get(nome='Inquietude')

	def testa_o_reconhecimento_de_uma_habilidade(self):
		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, self.feedback);
		reconhecimento = self.reconhecido.reconhecimentos()[0]

		self.assertEqual(1, len(self.reconhecido.reconhecimentos_por_valor(self.responsabilidade)))
		self.assertEqual(self.reconhecedor, reconhecimento.reconhecedor)
		self.assertEqual(self.responsabilidade, reconhecimento.valor)

	def testa_o_template_sci_no_reconhecimento(self):
		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, self.feedback)
		reconhecimento = self.reconhecido.reconhecimentos()[0]

		self.assertEqual(self.feedback.situacao, reconhecimento.feedback.situacao)
		self.assertEqual(self.feedback.comportamento, reconhecimento.feedback.comportamento)
		self.assertEqual(self.feedback.impacto, reconhecimento.feedback.impacto)

	def testa_que_armazena_a_data_do_reconhecimento(self):
		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, self.feedback);
		reconhecimento = self.reconhecido.reconhecimentos()[0]

		agora = timezone.now()
		self.assertEqual(agora.year, reconhecimento.data.year)
		self.assertEqual(agora.month, reconhecimento.data.month)
		self.assertEqual(agora.day, reconhecimento.data.day)

	def testa_a_listagem_de_reconhecimentos(self):
		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, self.feedback);
		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, self.feedback);

		valores_esperados = [self.responsabilidade, self.responsabilidade]
		valores_reconhecidos = map(lambda reconhecimento: reconhecimento.valor, self.reconhecido.reconhecimentos())
		self.assertEqual(valores_esperados, list(valores_reconhecidos))

	def testa_a_listagem_de_reconhecimentos_por_valor(self):
		self.reconhecido.reconhecer(self.reconhecedor, self.inquietude, self.feedback);
		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, self.feedback);
		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, self.feedback);

		self.assertEqual(1, len(self.reconhecido.reconhecimentos_por_valor(self.inquietude)))
		self.assertEqual(2, len(self.reconhecido.reconhecimentos_por_valor(self.responsabilidade)))

	def testa_que_o_colaborador_nao_pode_se_reconher(self):
		with self.assertRaises(Exception) as contexto:
			self.reconhecido.reconhecer(self.reconhecido, self.responsabilidade, self.feedback)

		self.assertEqual('O colaborador nao pode reconher a si próprio', contexto.exception.args[0])

	def testa_que_o_colaborador_nao_pode_reconhecer_com_justificativa_vazia(self):
		with self.assertRaises(Exception) as contexto:
			self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, None)

		self.assertEqual('Feedback deve ser informado', contexto.exception.args[0])

	def testa_que_existe_um_feedback(self):
		pass

	def testa_alteracao_de_um_feedback(self):
		reconhecimento = ReconhecimentoFactory(reconhecedor=self.reconhecedor)
		novo_feedback = FeedbackFactory()

		reconhecimento.alterar_feedback(novo_feedback, self.reconhecedor)

		self.assertEqual(novo_feedback, reconhecimento.feedback)

	def testa_que_nao_permite_alteracao_de_feedback_depois_de_1_dia(self):
		ontem = datetime.now() - timedelta(days=1)
		reconhecimento = ReconhecimentoFactory(reconhecedor=self.reconhecedor)
		reconhecimento.data = ontem
		novo_feedback = FeedbackFactory()

		with self.assertRaises(Exception) as contexto:
			reconhecimento.alterar_feedback(novo_feedback, self.reconhecedor)

		self.assertEqual('O reconhecimento só pode ser alterado no mesmo dia de sua realização', contexto.exception.args[0])

	def testa_que_o_feedback_so_pode_ser_alterado_por_quem_o_criou(self):
		reconhecimento = ReconhecimentoFactory()
		novo_feedback = FeedbackFactory()
		outro_reconhecedor = self.reconhecedor

		with self.assertRaises(Exception) as contexto:
			reconhecimento.alterar_feedback(novo_feedback, self.reconhecedor)

		self.assertEqual('O reconhecimento só pode ser alterado por quem o elaborou', contexto.exception.args[0])

	def testa_que_valor_sabe_retornar_uma_lista_de_frases_que_o_descreve_detalhadamente(self):
		descricao1 = DescricaoDoValorFactory(descricao="descricao1")
		descricao2 = DescricaoDoValorFactory(descricao="descricao2")
		valor = ValorFactory(descricoes=(descricao1, descricao2))

		detalhes = valor.frases_de_descricao

		self.assertEqual([descricao1.descricao, descricao2.descricao], detalhes)

class TesteDeFeedback(TestCase):
	def testa_que_deve_possuir_a_situacao_da_acao(self):
		situacao = "Situação cabulosa"

		feedback = Feedback.objects.create(situacao=situacao)

		self.assertEqual(feedback.situacao, situacao)

	def testa_que_deve_possuir_o_comportamento_da_acao(self):
		comportamento = "Você foi chato"

		feedback = Feedback.objects.create(comportamento=comportamento)

		self.assertEqual(feedback.comportamento, comportamento)

	def testa_que_deve_possuir_o_impacto_da_acao(self):
		impacto = "Profundo"

		feedback = Feedback.objects.create(impacto=impacto)

		self.assertEqual(feedback.impacto, impacto)

	def testa_que_deve_comparar_dois_feedbacks_pelos_seus_atributos(self):
		feedback = Feedback.objects.create(situacao='situacao1', comportamento='comportamento1', impacto='impacto1')
		outroFeedbackIgual = Feedback.objects.create(situacao='situacao1', comportamento='comportamento1', impacto='impacto1')
		outroFeedbackDiferente = Feedback.objects.create(situacao='situacao2', comportamento='comportamento2', impacto='impacto2')

		self.assertEqual(feedback, outroFeedbackIgual)
		self.assertNotEqual(feedback, outroFeedbackDiferente)