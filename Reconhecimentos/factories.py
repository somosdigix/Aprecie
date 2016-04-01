import factory
from Login.factories import ColaboradorFactory
from Reconhecimentos.models import Reconhecimento, Valor, DescricaoDoValor


class DescricaoDoValorFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = DescricaoDoValor

	descricao = factory.Iterator([
		"Indivíduos e interação entre eles mais que processos e ferramentas",
		"Software em funcionamento mais que documentação abrangente",
		"Colaboração com o cliente mais que negociação de contratos",
		"Responder a mudanças mais que seguir um plano"])

class ValorFactory(factory.django.DjangoModelFactory):

	class Meta:
		model = Valor

	nome = "Agilidade"
	resumo = "bla bla bla"

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
	valor = Valor.objects.get(nome='Alegria')
	justificativa = "uma justificativa qualquer"
	data = '2015-01-01'
