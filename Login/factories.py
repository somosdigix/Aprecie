from Reconhecimentos.models import Pilar
import factory
from Login.models import Colaborador
from datetime import datetime, timedelta
import random

def gerar_data_aleatoria():
	anos_atras = random.randint(20, 80) * 365
	return datetime.today() - timedelta(days=anos_atras)

class PilarFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Pilar

	nome = 'Fazer diferente'
	descricao = 'Descrição do pilar de fazer diferente'

class ColaboradorFactory(factory.django.DjangoModelFactory):

	class Meta:
		model = Colaborador

	cpf = factory.Sequence(lambda i: str(random.randint(10000000000, 99999999999)))
	nome = "Alberto Roberto"
	data_de_nascimento = factory.Sequence(lambda i: gerar_data_aleatoria())
