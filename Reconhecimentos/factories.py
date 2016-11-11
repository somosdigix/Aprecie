import factory
from Login.factories import ColaboradorFactory
from Reconhecimentos.models import *

class DescricaoDoValorFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = DescricaoDoValor

  descricao = factory.Iterator([
    'Indivíduos e interação entre eles mais que processos e ferramentas',
    'Software em funcionamento mais que documentação abrangente',
    'Colaboração com o cliente mais que negociação de contratos',
    'Responder a mudanças mais que seguir um plano'])

class ValorFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Valor

  nome = 'Agilidade'
  resumo = 'bla bla bla'

  @factory.post_generation
  def descricoes(self, create, extracted, **kwargs):
    if not create:
      return

    if extracted:
      for descricao in extracted:
        self.descricoes.add(descricao)

class ReconhecimentoFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Reconhecimento

  reconhecedor = factory.SubFactory(ColaboradorFactory)
  reconhecido = factory.SubFactory(ColaboradorFactory)
  pilar = Pilar.objects.get(nome='Colaborar sempre')
  feedback = factory.SubFactory('Reconhecimentos.factories.FeedbackFactory')
  data = '2015-01-01'

class ReconhecimentoHistoricoFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = ReconhecimentoHistorico

  reconhecedor = factory.SubFactory(ColaboradorFactory)
  reconhecido = factory.SubFactory(ColaboradorFactory)
  valor = Valor.objects.get(nome='Alegria')
  feedback = factory.SubFactory('Reconhecimentos.factories.FeedbackFactory')
  data = '2015-01-01'

class FeedbackFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Feedback

  situacao = 'Aquele dia...'
  comportamento = 'Você fez tal coisa...'
  impacto = 'E o cliente ficou chateado'
