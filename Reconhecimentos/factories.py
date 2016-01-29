import factory
from Login.factories import ColaboradorFactory
from Reconhecimentos.statics import ValoresDaDigithoBrasil
from Reconhecimentos.models import Reconhecimento

class ReconhecimentoFactory(factory.django.DjangoModelFactory):

	class Meta:
		model = Reconhecimento

	reconhecedor = factory.SubFactory(ColaboradorFactory)
	reconhecido = factory.SubFactory(ColaboradorFactory)
	valor = ValoresDaDigithoBrasil.inquietude
	justificativa = "uma justificativa qualquer"
	data = '2015-01-01'