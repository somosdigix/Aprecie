from datetime import date, datetime, timedelta
from django.test import TestCase

from Login.factories import ColaboradorFactory
from Reconhecimentos.models import *
from Reconhecimentos.factories import *

class TesteDeReconhecimento(TestCase):
  def setUp(self):
    self.feedback = FeedbackFactory()
    self.reconhecido = ColaboradorFactory()
    self.reconhecedor = ColaboradorFactory()
    self.responsabilidade = Valor.objects.get(nome='Responsabilidade')
    self.inquietude = Valor.objects.get(nome='Inquietude')

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

class TesteDeValor(TestCase):
  def testa_que_valor_sabe_retornar_uma_lista_de_frases_que_o_descreve_detalhadamente(self):
    descricao1 = DescricaoDoValorFactory(descricao="descricao1")
    descricao2 = DescricaoDoValorFactory(descricao="descricao2")
    valor = ValorFactory(descricoes=(descricao1, descricao2))

    detalhes = valor.frases_de_descricao

    self.assertEqual([descricao1.descricao, descricao2.descricao], detalhes)

class TesteDeFeedback(TestCase):
  def testa_que_deve_possuir_o_descritivo(self):
    descritivo = "Descritivo qualquer"

    feedback = Feedback.objects.create(descritivo=descritivo)

    self.assertEqual(feedback.descritivo, descritivo)

  def testa_que_deve_comparar_dois_feedbacks_pelos_seus_atributos(self):
    feedback = Feedback.objects.create(descritivo='descritivo1')
    outroFeedbackIgual = Feedback.objects.create(descritivo='descritivo1')
    outroFeedbackDiferente = Feedback.objects.create(descritivo='descritivo2')

    self.assertEqual(feedback, outroFeedbackIgual)
    self.assertNotEqual(feedback, outroFeedbackDiferente)

class TesteDoPilar(TestCase):
  def testa_que_deve_possuir_um_nome(self):
    nome = 'Colaborar sempre'

    pilar = Pilar.objects.create(nome = nome)

    self.assertEqual(pilar.nome, nome)

  def testa_que_deve_possuir_uma_descricao(self):
    descricao = 'Utilizar a colaboração para criar relacionamentos com foco em resultados para todos'

    pilar = Pilar.objects.create(descricao = descricao)

    self.assertEqual(pilar.descricao, descricao)

  def testa_que_deve_comparar_dois_pilares_pelo_nome(self):
    pilar = Pilar.objects.create(nome = 'Pilar')
    outroPilarIgual = Pilar.objects.create(nome = 'Pilar')
    outroPilarDiferente = Pilar.objects.create(nome = 'Pilar diferente')

    self.assertEqual(pilar, outroPilarIgual)
    self.assertNotEqual(pilar, outroPilarDiferente)
