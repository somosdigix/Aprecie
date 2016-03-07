import factory
from Login.factories import ColaboradorFactory
from Reconhecimentos.models import Reconhecimento, Valor

class ReconhecimentoFactory(factory.django.DjangoModelFactory):

	class Meta:
		model = Reconhecimento

	reconhecedor = factory.SubFactory(ColaboradorFactory)
	reconhecido = factory.SubFactory(ColaboradorFactory)
	valor = Valor.objects.get(nome='Alegria')
	justificativa = "uma justificativa qualquer"
	data = '2015-01-01'