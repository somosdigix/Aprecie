from django.test import TestCase
from django.utils import timezone
from Login.models import Colaborador
from Reconhecimentos.models import Reconhecimento, Valor
from Reconhecimentos.views import reconhecer
from Login.factories import ColaboradorFactory
from Reconhecimentos.factories import ReconhecimentoFactory
from Aprecie.base import ExcecaoDeDominio
from datetime import date, datetime, timedelta

class TesteDeReconhecimento(TestCase):

	def setUp(self):
		self.reconhecido = ColaboradorFactory()
		self.reconhecedor = ColaboradorFactory()
		self.responsabilidade = Valor.objects.get(nome='Responsabilidade')
		self.inquietude = Valor.objects.get(nome='Inquietude')

	def testa_o_reconhecimento_de_uma_habilidade(self):
		justificativa = 'Foi legal'

		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, justificativa);
		reconhecimento = self.reconhecido.reconhecimentos()[0]

		self.assertEqual(1, len(self.reconhecido.reconhecimentos_por_valor(self.responsabilidade)))
		self.assertEqual(self.reconhecedor, reconhecimento.reconhecedor)
		self.assertEqual(self.responsabilidade, reconhecimento.valor)
		self.assertEqual(justificativa, reconhecimento.justificativa)

	def testa_que_armazena_a_data_do_reconhecimento(self):
		justificativa = 'Gostei!'

		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, justificativa);
		reconhecimento = self.reconhecido.reconhecimentos()[0]

		agora = timezone.now()
		self.assertEqual(agora.year, reconhecimento.data.year)
		self.assertEqual(agora.month, reconhecimento.data.month)
		self.assertEqual(agora.day, reconhecimento.data.day)

	def testa_a_listagem_de_reconhecimentos(self):
		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, 'Foi legal');
		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, 'Voce realmente questiona as coisas');

		valores_esperados = [self.responsabilidade, self.responsabilidade]
		valores_reconhecidos = map(lambda reconhecimento: reconhecimento.valor, self.reconhecido.reconhecimentos())
		self.assertEqual(valores_esperados, list(valores_reconhecidos))
		
	def testa_a_listagem_de_reconhecimentos_por_valor(self):
		self.reconhecido.reconhecer(self.reconhecedor, self.inquietude, 'Foi legal');
		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, 'Voce realmente questiona as coisas');
		self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, 'Parabens pela iniciativa');

		self.assertEqual(1, len(self.reconhecido.reconhecimentos_por_valor(self.inquietude)))
		self.assertEqual(2, len(self.reconhecido.reconhecimentos_por_valor(self.responsabilidade)))

	def testa_que_o_colaborador_nao_pode_se_reconher(self):
		with self.assertRaises(Exception) as contexto:
			self.reconhecido.reconhecer(self.reconhecido, self.responsabilidade, 'Parabéns pela iniciativa')

		self.assertEqual('O colaborador nao pode reconher a si próprio', contexto.exception.args[0])

	def testa_que_o_colaborador_nao_pode_reconhecer_com_justificativa_vazia(self):
		with self.assertRaises(Exception) as contexto:
			self.reconhecido.reconhecer(self.reconhecedor, self.responsabilidade, '   ')

		self.assertEqual('A sua justificativa deve ser informada', contexto.exception.args[0])

	def testa_alteracao_de_uma_justificativa(self):
		reconhecimento = ReconhecimentoFactory(reconhecedor=self.reconhecedor, justificativa="Foi legal")
		nova_justificativa = 'Nova justificativa'

		reconhecimento.alterar_justificativa(nova_justificativa, self.reconhecedor)

		self.assertEqual(nova_justificativa, reconhecimento.justificativa)

	def testa_que_nao_permite_alteracao_de_justificativa_depois_de_1_dia(self):
		reconhecimento = ReconhecimentoFactory(reconhecedor=self.reconhecedor)
		ontem = datetime.now() - timedelta(days=1)
		reconhecimento.data = ontem
		nova_justificativa = 'Nova justificativa'

		with self.assertRaises(Exception) as contexto:
			reconhecimento.alterar_justificativa(nova_justificativa, self.reconhecedor)

		self.assertEqual('O reconhecimento só pode ser alterado no mesmo dia de sua realização', contexto.exception.args[0])

	def testa_que_nao_permite_alteracao_quando_for_editado_por_outra_pessoa_exceto_reconhecedor(self):
		reconhecimento = ReconhecimentoFactory()
		nova_justificativa = 'Nova justificativa'
		outro_reconhecedor = self.reconhecedor

		with self.assertRaises(Exception) as contexto:
			reconhecimento.alterar_justificativa(nova_justificativa, self.reconhecedor)

		self.assertEqual('O reconhecimento só pode ser alterado por quem o elaborou', contexto.exception.args[0])