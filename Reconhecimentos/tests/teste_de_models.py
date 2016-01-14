from django.test import TestCase
from django.utils import timezone
from Login.models import Funcionario
from Reconhecimentos.models import Valor
from Reconhecimentos.models import Reconhecimento
from Reconhecimentos.statics import ValoresDaDigithoBrasil
from Reconhecimentos.views import reconhecer
from Login.factories import FuncionarioFactory
from Reconhecimentos.factories import ReconhecimentoFactory
from Aprecie.base import ExcecaoDeDominio
from datetime import date, datetime, timedelta

class TesteDeReconhecimento(TestCase):

	def setUp(self):
		self.reconhecido = FuncionarioFactory()
		self.reconhecedor = FuncionarioFactory()

	def testa_o_reconhecimento_de_uma_habilidade(self):
		justificativa = 'Foi legal'

		self.reconhecido.reconhecer(self.reconhecedor, ValoresDaDigithoBrasil.inquietude, justificativa);
		reconhecimento = self.reconhecido.reconhecimentos()[0]

		self.assertEqual(1, len(self.reconhecido.reconhecimentos_por_valor(ValoresDaDigithoBrasil.inquietude)))
		self.assertEqual(self.reconhecedor, reconhecimento.reconhecedor)
		self.assertEqual(ValoresDaDigithoBrasil.inquietude, reconhecimento.valor)
		self.assertEqual(justificativa, reconhecimento.justificativa)

	def testa_que_armazena_a_data_do_reconhecimento(self):
		justificativa = 'Gostei!'

		self.reconhecido.reconhecer(self.reconhecedor, ValoresDaDigithoBrasil.responsabilidade, justificativa);
		reconhecimento = self.reconhecido.reconhecimentos()[0]

		self.assertEqual(timezone.now().year, reconhecimento.data.year)
		self.assertEqual(timezone.now().month, reconhecimento.data.month)
		self.assertEqual(timezone.now().day, reconhecimento.data.day)

	def testa_a_listagem_de_reconhecimentos(self):
		self.reconhecido.reconhecer(self.reconhecedor, ValoresDaDigithoBrasil.responsabilidade, 'Foi legal');
		self.reconhecido.reconhecer(self.reconhecedor, ValoresDaDigithoBrasil.inquietude, 'Voce realmente questiona as coisas');

		valores_esperados = [ValoresDaDigithoBrasil.responsabilidade, ValoresDaDigithoBrasil.inquietude]
		valores_reconhecidos = map(lambda reconhecimento: reconhecimento.valor, self.reconhecido.reconhecimentos())
		self.assertEqual(valores_esperados, list(valores_reconhecidos))
		
	def testa_a_listagem_de_reconhecimentos_por_valor(self):
		self.reconhecido.reconhecer(self.reconhecedor, ValoresDaDigithoBrasil.responsabilidade, 'Foi legal');
		self.reconhecido.reconhecer(self.reconhecedor, ValoresDaDigithoBrasil.inquietude, 'Voce realmente questiona as coisas');
		self.reconhecido.reconhecer(self.reconhecedor, ValoresDaDigithoBrasil.responsabilidade, 'Parabens pela iniciativa');

		self.assertEqual(1, len(self.reconhecido.reconhecimentos_por_valor(ValoresDaDigithoBrasil.inquietude)))
		self.assertEqual(2, len(self.reconhecido.reconhecimentos_por_valor(ValoresDaDigithoBrasil.responsabilidade)))

	def testa_que_o_colaborador_nao_pode_se_reconher(self):
		with self.assertRaises(Exception) as contexto:
			self.reconhecido.reconhecer(self.reconhecido, ValoresDaDigithoBrasil.responsabilidade, 'Parabéns pela iniciativa')

		self.assertEqual('O colaborador nao pode reconher a si próprio', contexto.exception.args[0])

	def testa_que_o_colaborador_nao_pode_reconhecer_com_justificativa_vazia(self):
		with self.assertRaises(Exception) as contexto:
			self.reconhecido.reconhecer(self.reconhecedor, ValoresDaDigithoBrasil.inquietude, '   ')

		self.assertEqual('A sua justificativa deve ser informada', contexto.exception.args[0])

	def testa_alteracao_de_uma_justificativa(self):
		justificativa = 'Foi legal'
		self.reconhecido.reconhecer(self.reconhecedor, ValoresDaDigithoBrasil.inquietude, justificativa);
		reconhecimento = self.reconhecido.reconhecimentos()[0]
		nova_justificativa = 'Nova justificativa'

		reconhecimento.alterar_justificativa(nova_justificativa)

		self.assertEqual(nova_justificativa, reconhecimento.justificativa)

	def testa_que_nao_permite_alteracao_de_justificativa_depois_de_1_dia(self):
		ontem = datetime.now() - timedelta(days=1)
		reconhecimento = ReconhecimentoFactory()
		reconhecimento.data = ontem
		nova_justificativa = 'Nova justificativa'

		with self.assertRaises(Exception) as contexto:
			reconhecimento.alterar_justificativa(nova_justificativa)

		self.assertEqual('O reconhecimento só pode ser alterado no mesmo dia de sua realização', contexto.exception.args[0])