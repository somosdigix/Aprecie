import factory
from Login.factories import ColaboradorFactory
from Reconhecimentos.models import *

class ReconhecimentoFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Reconhecimento

  reconhecedor = factory.SubFactory(ColaboradorFactory)
  reconhecido = factory.SubFactory(ColaboradorFactory)
  pilar = Pilar.objects.get(nome='Colaborar sempre')
  feedback = factory.SubFactory('Reconhecimentos.factories.FeedbackFactory')
  data = '2015-01-01'

class FeedbackFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Feedback

  descritivo = 'Você fez tal coisa...'

class FeedbackSCIFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Feedback

  situacao = 'Aquele dia...'
  comportamento = 'Você fez tal coisa...'
  impacto = 'E o cliente ficou chateado'

